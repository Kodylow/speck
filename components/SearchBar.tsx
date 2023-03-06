import { LightningInvoice, LNURLPAYDATA } from "@/types";
import { IconBolt, IconSearch } from "@tabler/icons-react";
import { useRef } from "react";

interface SearchBarProps {
  lnUrlPayData: LNURLPAYDATA | undefined;
  setInvoice: (invoice: LightningInvoice) => void;
  setShowModal: (showModal: boolean) => void;
  inputRef: React.RefObject<HTMLInputElement>;
  query: string;
  setQuery: (query: string) => void;
  handleKeyDown: (e: React.KeyboardEvent) => void;
  handleSearch: () => void;
}

export function SearchBar(props: SearchBarProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <div className="relative w-full mt-4 border border-gray-400 rounded-full flex items-center justify-between z-50">
      <IconSearch className="absolute top-3 w-10 left-1 h-6 rounded-full opacity-50 sm:left-3 sm:top-4 sm:h-8 text-black" />
      <div className="flex-grow">
        <input
          ref={inputRef}
          className="h-12 w-full rounded-full border-none px-11 focus:border-zinc-800 focus:outline-none focus:ring-1 focus:ring-zinc-800 sm:h-16 sm:py-2 sm:pr-16 sm:pl-16 sm:text-lg text-black"
          type="text"
          placeholder="What is a BOLT11 lightning invoice and how do I parse it?"
          value={props.query}
          onChange={(e) => props.setQuery(e.target.value)}
          onKeyDown={props.handleKeyDown}
        />
      </div>
      <IconBolt
        onClick={async () => {
          const response = await fetch(
            `${props.lnUrlPayData?.callback}?amount=1000000`
          );
          const invoice: LightningInvoice = await response.json();
          props.setInvoice(invoice);
          props.setShowModal(true);
        }}
        className="absolute top-3 right-1 h-6 w-6 rounded-full bg-yellow-500 flex items-center justify-center cursor-pointer sm:right-3 sm:top-4 sm:h-8 sm:w-8 hover:filter hover:invert"
      />
    </div>
  );
}
