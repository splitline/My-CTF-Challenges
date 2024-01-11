const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

const PORT = process.env.PORT || 3000;
const mongo = {
    host: process.env.MONGO_HOST || 'localhost',
    db: process.env.MONGO_DB || 'loginui',
};

app.get('/', (_, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/login', async (req, res) => {
    const db = app.get('db');
    const { username, password } = req.body;
    const user = await db.collection('users').findOne({ username, password });
    if (user) {
        res.send('success owo!');
    } else {
        res.send('failed qwq');
    }
});

const MongoClient = require('mongodb').MongoClient;

MongoClient.connect(mongo.host, (err, client) => {
    if (err) throw err;
    app.set('db', client.db(mongo.db));
    app.listen(PORT, () => console.log(`Listening on port ${PORT}`));
});
