import App from "./App";
import dotenv from "dotenv";
import mongooseInit from "./models";

dotenv.config();

// Setting Mongoose
(async function () {
  await mongooseInit();
})();

App.Start();
