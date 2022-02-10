import { model, Schema } from "mongoose";
import { RecoProcess } from "./types";

const schema = new Schema<RecoProcess>(
  {
    title: { type: String, required: true },
    dataName: { type: String, required: true },
    minPer: { type: Number, required: true },
    maxPer: { type: Number, required: true },
    step: { type: String, required: true },
    createdAt: { type: String, required: true },
    updatedAt: { type: String, required: true },
  },
  {
    collection: "process",
  }
);

const RecoProcessModel = model<RecoProcess>("process", schema);
export default RecoProcessModel;
