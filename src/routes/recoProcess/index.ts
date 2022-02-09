import express from "express";
import { Socket } from "socket.io";

class ProcessRoutes {
  routes: express.Router;

  constructor() {
    this.routes = express.Router();
    this.SetRoutes();
  }

  SetRoutes() {
    this.routes.patch("/", (req: express.Request, res: express.Response) => {
      const body = <UpdateProcess>req.body;
      console.log(body);

      const socket = req.app.get("socket") as Socket;
      socket.emit("alert", {
        ...body,
      });

      return res.status(200).json({
        status: true,
        message: "해당 프로세스가 업데이트 되었습니다.",
      });
    });
  }
}
export default new ProcessRoutes().routes;
