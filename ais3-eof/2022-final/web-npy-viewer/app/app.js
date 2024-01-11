const express = require('express');
const fileUpload = require('express-fileupload');
const nunjucks = require('nunjucks');

const npyz = require('npyz');

const fs = require('fs');
const os = require('os');

const app = express();
const tmpUploadDir = fs.mkdtempSync(os.tmpdir())
const TEMPLATE = `
<h1>Upload a .npy / .npz file</h1>
<p>Reference: https://numpy.org/devdocs/reference/generated/numpy.lib.format.html</p>
<form action="/" method="POST" enctype="multipart/form-data">
<input type="file" name="file" />
<input type="submit" value="Upload" />
</form>

<h2>Result</h2>
<pre>{{ result }}</pre>
`;

app.use(fileUpload({
    preserveExtension: true,
    limits: { fileSize: 50 * 1024 * 1024 },
}));

app.get('/', (_, res) => {
    return res.send(nunjucks.renderString(TEMPLATE, {
        result: "(You haven't upload any file)"
    }));
});

app.post('/', function (req, res) {
    if (!req.files || !req.files.file)
        return res.status(400).send('No files were uploaded.');


    const uploadPath = `${tmpUploadDir}/${+new Date()}-${req.files.file.name}`;
    const npyFile = req.files.file;

    npyFile.mv(uploadPath, function (err) {
        if (err) return res.status(500).send(err.toString());

        npyz.load(uploadPath).then((data) => {
            const html = nunjucks.renderString(TEMPLATE, { result: JSON.stringify(data, null, 2) });
            return res.send(html);
        }).catch(err => {
            return res.status(500).send(err.toString());
        }).finally(() => fs.unlinkSync(uploadPath));
    });
});


app.listen(3000);