import { LightningInvoice } from "@/types";
import { IconCircleCheck } from "@tabler/icons-react";
import QRCode from "qrcode.react";
import { useEffect, useState } from "react";

type LightningModalProps = {
  lightningInvoice: LightningInvoice;
  setShowModal: (showModal: boolean) => void;
  onSuccess: () => void;
};

export function LightningModal({
  lightningInvoice,
  setShowModal,
  onSuccess,
}: LightningModalProps) {
  const [status, setStatus] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isReady, setIsReady] = useState(false);

  const handleCopyClick = () => {
    navigator.clipboard.writeText(lightningInvoice.pr);
  };

  const handleOpenClick = () => {
    window.open(`lightning:${lightningInvoice.pr}`);
  };

  useEffect(() => {
    let interval: NodeJS.Timeout;

    const verifyPayment = async () => {
      try {
        const response = await fetch(lightningInvoice.verify);
        const result = await response.json();

        if (result.settled) {
          setStatus("success");
          clearInterval(interval);
          onSuccess(); // call onSuccess callback function
          setTimeout(() => setShowModal(false), 2000);
        } else {
          setStatus("pending");
        }
      } catch (error) {
        setStatus("error");
        setErrorMessage("Failed to verify payment.");
        clearInterval(interval);
      }
    };

    setIsReady(true);
    interval = setInterval(verifyPayment, 1000);
    return () => clearInterval(interval);
  }, [lightningInvoice, setShowModal]);

  let content = (
    <div className="w-64 h-64 relative">
      <QRCode
        value={lightningInvoice.pr}
        size={256}
        onClick={handleCopyClick}
        className="w-full h-full absolute cursor-pointer"
      />
    </div>
  );

  if (status === "success") {
    content = (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: 256,
          height: 256,
        }}
      >
        <IconCircleCheck size={128} stroke={3} color="green" />
      </div>
    );
  }

  return (
    <>
      {isReady && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
          <div className="modal-content bg-white shadow-lg rounded-md p-4 flex flex-col">
            <span
              onClick={() => setShowModal(false)}
              className="close cursor-pointer text-2xl text-gray-500 hover:text-gray-700"
            >
              &times;
            </span>
            <div className="content-container flex justify-center p-4">
              {content}
            </div>
            <div className="flex justify-center">
              <button
                id="copy-button"
                className="border border-gray-300 text-gray-700 px-4 py-2 rounded-l-md hover:bg-gray-100 focus:outline-none focus:shadow-outline-blue active:bg-gray-200 transition duration-150 ease-in-out"
                onClick={handleCopyClick}
              >
                Copy
              </button>
              <button
                id="open-button"
                className="border border-gray-300 text-white bg-yellow-500 px-4 py-2 rounded-r-md hover:bg-yellow-600 focus:outline-none focus:shadow-outline-blue active:bg-yellow-700 transition duration-150 ease-in-out"
                onClick={handleOpenClick}
              >
                Open in ⚡ Wallet
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
