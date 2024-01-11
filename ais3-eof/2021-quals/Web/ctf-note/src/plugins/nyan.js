(function () {
    const nyanCatURL = "/static/nyancat.gif";
    document.querySelectorAll("p.title:not(.is-4)")
        .forEach(title => {
            const img = document.createElement("img");
            img.src = nyanCatURL;
            img.style.height = '2rem';
            title.appendChild(img);
        });
})();
