export enum OpenAIModel {
  DAVINCI_TURBO = "gpt-3.5-turbo",
}

export type LNURLPAYDATA = {
  status: string;
  tag: string;
  commentAllowed: number;
  callback: string;
  metadata: string;
  minSendable: number;
  maxSendable: number;
  payerData: {
    name: { mandatory: boolean };
    email: { mandatory: boolean };
  };
  nostrPubkey: string;
  allowsNostr: boolean;
};

export type LightningInvoice = {
  status: string;
  successAction: {
    tag: string;
    message: string;
  };
  verify: string;
  routes: any[]; // You can replace this with a more specific type if needed
  pr: string;
};
