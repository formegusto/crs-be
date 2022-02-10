import http from "http";
import express from "express";
import morgan from "morgan";
import SocketConnect from "./Socket";
import routes from "./routes";
import cors from "cors";
import mongooseInit from "./models";

class App {
  server: http.Server;
  app: express.Application;

  constructor() {
    this.app = express();

    this.SettingMW();
    this.SetRoutes();

    this.server = http.createServer(this.app);
  }

  SettingMW() {
    this.app.use(cors());
    this.app.use(morgan("dev"));
    this.app.use(express.json());
  }

  SetRoutes() {
    this.app.use(routes);
  }

  Start() {
    const port = process.env.PORT || "8080";
    this.server.listen(port, () => {
      console.log("[Server] Start Express :)\n" + `port no : ${port}\n`);
    });

    SocketConnect(this.server, this.app);
  }
}

export default new App();
