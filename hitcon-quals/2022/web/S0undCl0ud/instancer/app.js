const express = require('express');
const bodyParser = require('body-parser');
const { createProxyMiddleware } = require('http-proxy-middleware');
const session = require('express-session');

const child_process = require('child_process');
const crypto = require('crypto');
const net = require('net');

const hcaptcha = require('./hcaptcha');


// configuration

const TITLE = process.env.TITLE || 'Challenge Instancer'
const INSTANCER_HOST = process.env.INSTANCER_HOST || 'sandbox.local';
const CHALL_BASE_HOST = process.env.CHALL_BASE_HOST || '.test.splitline.tw';
const AUTO_DESTROY = +process.env.AUTO_DESTROY || 10; // in ... minutes
const HCAPTCHA_SITE_KEY = process.env.HCAPTCHA_SITE_KEY || '10000000-ffff-ffff-ffff-000000000001'


// utils

const genInstanceId = () => crypto.randomInt(2 ** 47, 2 ** 48).toString(36);
async function getPort() {
    return new Promise(res => {
        const srv = net.createServer();
        srv.listen(0, () => {
            const port = srv.address().port
            srv.close((err) => res(port))
        });
    })
}

const instanceIdToPort = new Map();


// reverse proxy

const reverseProxy = express();
reverseProxy.use(
    createProxyMiddleware({
        changeOrigin: true,
        router: function (req) {
            const hostname = req.hostname;
            if (hostname === INSTANCER_HOST)
                return `http://127.0.0.1:8000`;
            const re = RegExp('(\\w+)' + CHALL_BASE_HOST.replaceAll('.', '\\.'));
            if ((sub = re.exec(hostname)?.[1]) && instanceIdToPort.has(sub))
                return `http://127.0.0.1:${instanceIdToPort.get(sub)}`;
            return `http://127.0.0.1:8000/_noexists`;
        }
    })
);

reverseProxy.listen(80); // exposed


// instancer

const instancer = express();
instancer.use(bodyParser.urlencoded({ extended: false }));
instancer.use(session({
    secret: crypto.randomBytes(20).toString('hex'),
    resave: true,
    saveUninitialized: false
}));


instancer.get('/', (req, res) => {
    return res.send(`
<!DOCTYPE html>
<head>
<title>${TITLE}</title>
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
<style>body{font-family: Menlo, Consolas, Monaco, 'Liberation Mono', 'Lucida Console', monospace;}</style>
</head>
<body>
    <main>
    <h1>${TITLE}</h1>
    <article>
    ${!req.session.instanceId || new Date() > req.session.expiredAt ? `
    <form action="/create" method="POST" style="text-align: center">
        <input type="text" name="captcha" style="display: none">
        <input type="submit" value="Create New Instance">
        <div class="h-captcha" data-sitekey="${HCAPTCHA_SITE_KEY}"></div>
    </form>` : (`
    <p>Your instance can be accessed here:
        <a href="//${req.session.instanceId + CHALL_BASE_HOST}">${req.session.instanceId + CHALL_BASE_HOST}</a>
    </p>
    <p>Stopping at: <span id="stop"></span></p>
    <form action="/stop" method="POST" style="text-align: center">
        <input type="submit" value="Stop" style="background-color:red">
    </form>
    <script>
    const fmt = new Intl.DateTimeFormat([], { dateStyle: 'medium', timeStyle: 'long' });
    document.getElementById('stop').textContent = fmt.format(${req.session.expiredAt});
    </script>`)}
    </article>
    <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
    </main>
</body>
`);
})

instancer.get('/_noexists*', (req, res) => {
    res.redirect(`${req.protocol}://${INSTANCER_HOST}`);
})

instancer.post('/stop', (req, res) => {
    const instanceId = req.session.instanceId;
    if (!instanceId || !/^\w+$/.test(instanceId)) return res.redirect('/');

    const command = `docker stop ${instanceId} && docker rm ${instanceId}`;
    child_process.exec(command, (err) => {
        instanceIdToPort.delete(instanceId);
        req.session.destroy();
        res.redirect('/');
    });
})

instancer.post('/create', hcaptcha, async (req, res) => {
    let instanceId = genInstanceId();
    while (instanceIdToPort.has(instanceId)) {
        instanceId = genInstanceId();
    }
    const port = await getPort();
    instanceIdToPort.set(instanceId, port);
    setTimeout(() => instanceIdToPort.delete(instanceId), AUTO_DESTROY * 60 * 1000);

    const command = `docker run --name ${instanceId} -d --rm -e AUTO_DESTROY=${AUTO_DESTROY} -p ${port}:5000 service:latest`;
    child_process.exec(command, (err) => {
        if (err)
            return res.send(`<b>Oops, something wrong: </b><pre>${err}</pre> (please report this error message to the challenge author)`)
        req.session.instanceId = instanceId;
        req.session.expiredAt = +new Date() + AUTO_DESTROY * 60 * 1000;
        res.redirect('/');
    });
});

instancer.listen(8000); // internal
