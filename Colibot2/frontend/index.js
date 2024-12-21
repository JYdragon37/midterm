const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// 정적 파일 경로 수정
app.use(express.static(path.join(__dirname, '../backend/frontend/public')));
app.use('/weather', express.static(path.join(__dirname, '../backend/frontend/public/weather')));

app.get('/', async (req, res) => {
    try {
        const trending = await axios.get('http://localhost:5001/trending-csv')
            .catch(err => {
                console.error('Trending error:', err.message);
                return { data: [] };
            });

        const news = await axios.get('http://localhost:5001/news')
            .catch(err => {
                console.error('News error:', err.message);
                return { data: [] };
            });

        const weather = await axios.get('http://localhost:5001/weather')
            .catch(err => {
                console.error('Weather error:', err.message);
                return { data: { screenshot: '' } };
            });

        res.render('index', {
            trending: trending.data,
            news: news.data,
            weatherImage: weather.data.screenshot,
        });
    } catch (error) {
        console.error('Error details:', error);
        res.status(500).send('Error fetching data: ' + error.message);
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Express server running on port ${PORT}`);
});