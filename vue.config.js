const fs = require("fs");

module.exports = {
    outputDir: "dist",
    assetsDir: "static",
    devServer: {
        proxy: {
            "/api*": {
                target: "http://localhost:8000/",
            },
        },
    },
    css: {
        loaderOptions: {
            sass: {
                additionalData: fs.readFileSync("src/assets/scss/app.scss", "utf-8"),
            },
        },
    },
};
