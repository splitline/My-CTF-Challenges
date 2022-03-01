const express = require('express')
const bodyParser = require('body-parser')
const https = require('https')
const child_process = require('child_process')
const crypto = require('crypto')

const app = express()
app.use(bodyParser.urlencoded({ extended: false }))

const ctfdHost = process.env['CTFD_HOST'] || 'chal.ctf.tsj.tw'
const TEAMS = {}
const rateLimit = 10 // minutes

const getPassword = teamId =>
	crypto
		.createHash('sha256')
		.update(`!ypeBE@|$sobvc?` + teamId)
		.digest('base64')
		.slice(0, 16)

app.get('/', (req, res) => {
	return res.send(`
<h1>Genie Instance Creator</h1>
<form action="/create_instance" method="POST">
    <input type="text" name="token" placeholder="CTFd access token" />
    <button type="submit">Create Instance</button>
</form>
<p>You can get your token from <a href="http://${ctfdHost}/settings#tokens">here</a>.</p>
<p>Instance will shutdown in 10 minutes.</p>
`)
})

app.post('/create_instance', (req, res) => {
	const token = req.body.token + ''
	if (!token.match(/^[0-9a-f]{64}$/)) return res.status(400).send('invalid token')

	https.get(
		`https://${ctfdHost}/api/v1/users/me`,
		{
			headers: {
				Authorization: `Token ${token}`,
				'Content-Type': 'application/json'
			}
		},
		resp => {
			let rawData = ''
			resp.setEncoding('utf8')
			resp.on('data', chunk => {
				rawData += chunk
			})
			resp.on('end', () => {
				try {
					const parsedData = JSON.parse(rawData)
					if (!parsedData.success) {
						return res.status(400).send('Invalid token')
					}
					const teamId = +parsedData.data.team_id
					const port = teamId + 10000
					const password = getPassword(teamId)
					const url = `http://team${teamId}:${password}@${req.hostname}:${port}/`

					// Rate limit: 10 minuites
					if (teamId in TEAMS) {
						const timeDiff = new Date() - TEAMS[teamId]
						if (timeDiff < rateLimit * 60 * 1000) {
							const remainSeconds = (rateLimit * 60 * 1000 - timeDiff) / 1000
							return res
								.status(400)
								.send(
									`<p>Your team can create another instance after ${remainSeconds} seconds.</p>` +
										`<p>You might still be able to access the instance at <a href="${url}">${url}</a>.</p>`
								)
						}
					}

					TEAMS[teamId] = +new Date()
					const command = `docker run -d --rm -p ${port}:3000 --env USERNAME=team${teamId} --env PASSWORD=${password} service:latest`
					child_process.exec(command, err =>
						res.send(
							'<h1>Done</h1>' +
								`<pre>${command}</pre>` +
								(err
									? `<b>${err.toString()}</b> (Report this error message to author if you see this)`
									: '') +
								`<p>Success! Your can access your instance at <a href="${url}">${url}</a></p>`
						)
					)
				} catch (e) {
					console.error(e)
					res.status(500).send('Something went wrong')
				}
			})
		}
	).on('error', e => {
		res.status(500).send('Something went wrong')
	})
})

app.listen(8000)
console.log('Server started')
