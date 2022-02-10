import App from "./App";
import dotenv from "dotenv";
import mongooseInit from "./models";
import moment from "moment-timezone";

moment.tz.setDefault("Asia/Seoul");
dotenv.config();

// Setting Mongoose
(async function () {
  await mongooseInit();
})();

App.Start();
