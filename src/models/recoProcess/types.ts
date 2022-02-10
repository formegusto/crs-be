export type RecoProcess = {
  title: string;
  dataName: string;
  minPer: number;
  maxPer: number;
  step:
    | "init"
    | "start"
    | "load-excel"
    | "data-preprocessing"
    | "bill-calc"
    | "normal-analysis"
    | "mean-analysis"
    | "similarity-analysis";
  createdAt: string;
  updatedAt: string;
};
