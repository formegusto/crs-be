import express from "express";
import multer from "multer";
import path from "path";
import RecoProcessModel from "../models/recoProcess";
import { RecoProcess } from "../models/recoProcess/types";
import childProcess from "child_process";
import recoProcess from "./recoProcess";

class Routes {
  routes: express.Router;
  upload: express.RequestHandler;

  constructor() {
    this.routes = express.Router();
    this.upload = multer({
      storage: multer.diskStorage({
        destination: (req, file, cb) => {
          cb(null, "static");
        },
        filename: (req, file, cb) => {
          cb(
            null,
            `original-data-${Date.now()}${path.extname(file.originalname)}`
          );
        },
      }),
    }).single("data");

    this.SetRoutes();
  }

  SetRoutes() {
    this.routes.use("/process", recoProcess);
    this.routes.post(
      "/",
      this.upload,
      async (req: express.Request, res: express.Response) => {
        const filename = req.file?.filename;

        if (filename) {
          const regist: RecoProcess = {
            ...req.body,
            dataName: filename,
            step: "load excel",
          };

          const recoProcessInfo = await RecoProcessModel.create(regist);
          const id = recoProcessInfo.id;

          const recoProcess = childProcess.spawn("python3", [
            "python/reco_process.py",
            filename,
          ]);

          recoProcess.stdout.on("data", (data) => {
            console.log(data.toString());
          });

          recoProcess.stderr.on("data", (data) => {
            console.log("error 발생!");
            console.log(data.toString());
          });

          return res.status(200).json({
            status: true,
            message: "추천 서비스를 시작합니다.",
            datas: {
              registData: recoProcessInfo.toJSON(),
            },
          });
        }

        return res.status(400).json({
          status: false,
          message: "파일을 반드시 보내주셔야 합니다.",
        });
      }
    );
  }
}

export default new Routes().routes;
