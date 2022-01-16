const RAW_MARKDOWN_URL = `${location.pathname}/raw`;

(function () {
    const modal = document.querySelector(".modal");
    const modalBody = document.querySelector(".modal .modal-body");
    const modalClose = document.querySelector(".modal .close");

    modalClose.onclick = () => modal.hidden = true;

    const navItems = document.querySelectorAll("nav>.nav-item");

    // share button
    navItems[0].addEventListener("click", () => {
        modal.hidden = false;
        modalBody.innerHTML = `<h2>Share this note</h2>
        <p>Copy the following link and share it with your friends.</p>
        <input type="text" value="${GistMD.url}" readonly>`;
    });

    // show raw markdown
    navItems[1].addEventListener("click", () => {
        modal.hidden = false;
        modalBody.innerHTML = "<h2>Raw Markdown</h2><textarea readonly>Loading...</textarea>";
        fetch(RAW_MARKDOWN_URL).then(r => r.text()).then(text => {
            modalBody.querySelector("textarea").innerHTML = text;
        });
    });

    // report button
    navItems[2].addEventListener("click", () => {
        if (confirm("Report this note?")) {
            grecaptcha.ready(function () {
                grecaptcha.execute('6Lcn9Q4eAAAAAKxGpQjhjkTnOD6RS_NTXQojxOUu', { action: 'submit' }).then(function (token) {
                    document.getElementById('g-recaptcha-response').value = token;
                    document.getElementById('report-form').submit();
                });
            });
        }
    });


    // initialize markdown content
    window.onload = function () {
        fetch(RAW_MARKDOWN_URL).then(r => r.text()).then(markdown => {
            const html = DOMPurify
                .sanitize(marked.parse(markdown))
                .replace(/{%gist\s*(\S+)\s*%}/g, (_, gistId) => `
                <iframe 
                    class="gist-embed"
                    sandbox="allow-scripts allow-same-origin"
                    scrolling="no" data-gist="${encodeURI(gistId)}"
                    csp="default-src 'none'; style-src 'unsafe-inline' https://github.githubassets.com/assets/; script-src https://gist.github.com/;">
                </iframe>`);

            document.querySelector('.main').innerHTML = html;
            document.querySelector('.main').querySelectorAll('.gist-embed').forEach(embed => {
                embed.srcdoc = `<script src="https://gist.github.com/${embed.dataset.gist}.js"></script>`
                embed.onload = () =>
                    embed.style.height = `${embed.contentDocument.documentElement.scrollHeight}px`;
            });
        });

        document.getElementById('note-title').textContent = GistMD.title || GistMD.id;
    };

})();
