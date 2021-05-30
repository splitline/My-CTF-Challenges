<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

    <title>Web Challenges Monitor</title>
    <style>
        .container {
            width: auto;
            max-width: 680px;
            padding: 0 15px;
        }

        a,
        a:hover {
            text-decoration: none;
        }
    </style>
</head>

<body class="d-flex flex-column h-100">

    <!-- Begin page content -->
    <main class="flex-shrink-0">
        <div class="container">
            <h1 class="mt-5">Web Challenges Monitor</h1>
            <p class="lead">一個用來檢查 AIS3 Pre-Exam / MyFirstCTF 2021 的 Web 題是不是還活著的小工具 🐱</p>
            <hr>
            <ol id="challenges" class="list-group list-group-numbered"></ol>
        </div>
    </main>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        fetch("/?module=modules/api")
            .then(r => r.json())
            .then(json => json.forEach(data => {
                const url = `${data.host}:${data.port}`;
                const li = document.createElement("li");
                li.className = "list-group-item d-flex justify-content-between align-items-center";

                const infoDiv = document.createElement("li");
                infoDiv.className = "ms-2 me-auto";
                infoDiv.innerHTML = `<div class="fw-bold">${data.name}</div><a href="//${url}" class="link-secondary" target="_blank">${url}</a>`;

                const check = document.createElement("button");
                check.className = "btn btn-primary";
                check.textContent = 'Check!';
                check.onclick = () => {
                    check.disabled = true;
                    fetch(`/?module=modules/api&id=${data.id}`).then(r => r.json())
                        .then(({
                            alive
                        }) => {
                            check.className = `btn btn-${alive ? 'success' : 'danger'}`
                            check.textContent = alive ? '還活著！' : '死了 \\|/';
                            check.disabled = false;
                        });
                }

                li.append(infoDiv, check);
                challenges.appendChild(li);
            }));
    </script>
</body>

</html>