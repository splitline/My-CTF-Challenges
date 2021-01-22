/**
 * 原本沒有想讓大家讀著麼多 code 的，但為了設計出合理的場景只好 (ry
 * 不過其實大部分都是在刻 UI，跟題目沒直接關係，我有試著盡量加註解了 XD
 */

function loadPlugin(pluginName) {
    if (!(pluginName in CONFIG.plugins)) return;
    let script = document.createElement('script');
    script.src = CONFIG.plugins[pluginName];
    document.body.appendChild(script);
}

function render() {
    document.querySelector('[name="url"]').value = document.location;
    document.getElementById('content').innerHTML = "";

    if (location.hash.length <= 1) {
        // 首頁：列出所有 CTF
        document.getElementById("add-ctf").style.display = 'block';
        document.getElementById("report-ctf").style.display = 'none';
        document.getElementById("ctf-note-title").textContent = "Index of write-ups/";

        const tiles = document.createElement('div');
        tiles.className = 'tile is-vertical';
        fetch("/api/list")
            .then(r => r.json())
            .then(({ ctf }) => {
                ctf.forEach(({ title, uuid }) => {
                    const titleText = document.createElement("p");
                    titleText.className = "title is-4";
                    titleText.textContent = title;

                    const uuidText = document.createElement("span");
                    uuidText.className = 'tag is-info';
                    uuidText.textContent = uuid;

                    const anchor = document.createElement("a");
                    anchor.className = 'notification';
                    anchor.href = `/#${uuid}`;
                    anchor.append(titleText, uuidText);
                    tiles.appendChild(anchor);
                });
            });
        document.getElementById("content").appendChild(tiles);
    } else {
        // 單個 CTF 的 write-up
        document.getElementById("add-ctf").style.display = 'none';
        document.getElementById("report-ctf").style.display = 'block';
        const ctfId = location.hash.slice(1); // uuid
        const WriteUps = {
            Web: {},
            Reverse: {},
            Pwn: {},
            Crypto: {},
            Misc: {}
        };

        fetch(`/api/${ctfId}`)
            .then(resp => resp.json())
            .then(ctf => {
                // 標題：比賽名稱
                document.getElementById("ctf-note-title").textContent = ctf.contestName;
                ctf.writeups.forEach(writeup => {
                    if (!(writeup.category in WriteUps)) return;
                    WriteUps[writeup.category][writeup.challenge] = writeup.content;
                });

                const fragment = document.createDocumentFragment();
                Object.keys(WriteUps).forEach(category => {
                    // 題目類別的標題 (Web, Pwn etc.)
                    const categoryTitle = document.createElement("p");
                    categoryTitle.className = "title";
                    categoryTitle.textContent = category;
                    fragment.appendChild(categoryTitle);

                    // 按照類別顯示 write-up
                    Object.keys(WriteUps[category]).forEach(challenge => {
                        // 題目名稱
                        const challengeTitle = document.createElement("p");
                        challengeTitle.className = "title is-4";
                        challengeTitle.textContent = challenge;
                        fragment.appendChild(challengeTitle);

                        // 題目 write-up
                        const challengeContent = document.createElement("div");
                        challengeContent.className = "box"
                        challengeContent.innerHTML = markdown.toHTML(WriteUps[category][challenge]);
                        fragment.appendChild(challengeContent);
                    });
                });
                document.getElementById("content").appendChild(fragment);
                return fetch("/api/enabled_plugins")
            })
            .then(r => r.json())
            .then(plugins => plugins.forEach(loadPlugin));
    };
}


// 以下的東西應該就跟解題沒關係了，刻 UI 真的好累ㄛ

document.addEventListener('DOMContentLoaded', render, false);
window.addEventListener("hashchange", render, false);

document.getElementById("add-challenge").addEventListener("click", function () {
    const template = document.getElementById("challenge-template");
    const challenge = document.importNode(template.content, true);
    challenge.querySelector(".delete-challenge").onclick = event => event.target.closest(".challenge").remove();
    document.getElementById("challenge-container").appendChild(challenge);
});

document.getElementById("add-ctf").addEventListener("click", function () {
    document.querySelector(".modal").classList.add('is-active');
});

document.querySelector(".modal-close").addEventListener("click", function () {
    document.querySelector(".modal").classList.remove('is-active');
});

document.querySelector(".modal #submit").addEventListener("click", function () {
    const contestName = document.querySelector('.modal [name=contestName]').value;
    const writeups = [...document.querySelectorAll('.modal .challenge')].map(elem => Object.fromEntries(new FormData(elem)));
    fetch("/api/add", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ contestName, writeups })
    })
        .then(r => r.json())
        .then(({ uuid }) => {
            document.querySelector(".modal").classList.remove('is-active');
            location = `/#${uuid}`;
        });
});
