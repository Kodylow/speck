import { Footer } from "@/components/Footer";
import { LightningModal } from "@/components/LightningModal";
import { Navbar } from "@/components/Navbar";
import { ParticlesBackground } from "@/components/ParticlesBackground";
import { SearchBar } from "@/components/SearchBar";
import { LightningInvoice, LNURLPAYDATA } from "@/types";
import Head from "next/head";
import { useEffect, useRef, useState } from "react";
import { Light as SyntaxHighlighter } from "react-syntax-highlighter";
import { prism } from "react-syntax-highlighter/dist/cjs/styles/prism";
import { Tab, TabList, TabPanel, Tabs } from "react-tabs";
import "react-tabs/style/react-tabs.css";

const apiKey = process.env.OPENAI_API_KEY || "";
const lnAddress = "kodylow@getalby.com";

interface BIPSearchResult {
  metadata: SearchResult["metadata"];
  page_content: string;
}

interface CodeResult {
  metadata: {
    doc_type: string;
    filepath: string;
    length: number;
    slug: string;
  };
  page_content: string;
}

interface SearchResult {
  lookup_index: number;
  lookup_str: string;
  metadata: {
    Author: string;
    BIP: string;
    "Comments-Summary": string;
    "Comments-URI": string;
    Created: string;
    Layer: string;
    License: string;
    Status: string;
    Title: string;
    Type: string;
    filepath: string;
    length: number;
    tokens: number;
  };
  page_content: string;
}

interface Message {
  content: string;
  role: string;
}

interface Choice {
  finish_reason: string;
  index: number;
  message: Message;
}

interface GeneratedText {
  choices: Choice[];
  created: number;
  id: string;
  model: string;
  object: string;
  usage: {
    completion_tokens: number;
    prompt_tokens: number;
    total_tokens: number;
  };
}

interface ParsedSearchResults {
  bips: SearchResult[];
  bolts: SearchResult[];
  coreln: CodeResult[];
  lnd: CodeResult[];
  rustln: CodeResult[];
  generated_text?: GeneratedText;
}

export default function Home() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [showModal, setShowModal] = useState(false);
  const [query, setQuery] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [parsedSearchResults, setParsedSearchResults] =
    useState<ParsedSearchResults>({
      bips: [],
      bolts: [],
      coreln: [],
      lnd: [],
      rustln: [],
    });

  const [mode, setMode] = useState<"search" | "chat">("chat");
  const [matchCount, setMatchCount] = useState<number>(5);

  const [lnUrlPayData, setLnUrlPayData] = useState<LNURLPAYDATA>();
  const [invoice, setInvoice] = useState<LightningInvoice>();

  useEffect(() => {
    async function fetchLnUrlPayData() {
      const [username, host] = lnAddress.split("@");
      const url = `https://${host}/.well-known/lnurlp/${username}`;
      const response = await fetch(url);
      const data = await response.json();
      console.log(data);
      setLnUrlPayData(data);
    }

    fetchLnUrlPayData();
  }, []);

  const handleSearch = async () => {
    if (!query) {
      alert("Please enter a query.");
      return;
    }

    setAnswer("");

    // fetch and set search results
    const similaritySearchResponse = await fetch(
      `http://localhost:4080/similarity_search?query=${query}`
    );

    if (!similaritySearchResponse.ok) {
      throw new Error(similaritySearchResponse.statusText);
    }

    const searchResults: ParsedSearchResults =
      await similaritySearchResponse.json();
    console.log("searchResults:", searchResults);
    setParsedSearchResults(searchResults);
  };

  const handleKeyDown = (e: KeyboardEvent<Element>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <>
      {showModal && invoice && (
        <LightningModal
          lightningInvoice={invoice}
          setShowModal={setShowModal}
          onSuccess={() => {}}
        />
      )}
      <Head>
        <title>SPECK</title>
        <meta
          name="description"
          content={`AI-powered search and chat for Tim Urban's blog "Wait But Why."`}
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/boltsPic.ico" />
      </Head>
      <ParticlesBackground />
      <div className="flex flex-col h-screen text-white">
        <Navbar />
        <div className="flex-1 overflow-auto">
          <div className="mx-auto flex h-full w-full max-w-[750px] flex-col items-center px-3 pt-4 sm:pt-8">
            <div className="mx-auto w-full max-w-[750px] text-center">
              <h1 className="text-4xl font-bold mb-4">SPECK</h1>
              <h3 className="text-2xl font-medium">
                The Reckless Bitcoin Lightning Specification Bot
              </h3>
            </div>

            <SearchBar
              query={query}
              setQuery={setQuery}
              inputRef={inputRef}
              lnUrlPayData={lnUrlPayData}
              setInvoice={setInvoice}
              setShowModal={setShowModal}
              handleSearch={handleSearch}
              handleKeyDown={handleKeyDown}
            />

            <div className="max-w-screen-md mx-auto">
              {Object.values(parsedSearchResults).some(
                (array) => array.length > 0
              ) &&
                parsedSearchResults.generated_text?.choices[0] && (
                  <div className="mt-4 text-black">
                    <h4 className="font-bold pb-2">Generated Text</h4>
                    <div className="px-4 py-2 bg-gray-100 rounded-md overflow-y-auto max-h-60">
                      <span className="whitespace-pre-line overflow-wrap break-words">
                        {
                          parsedSearchResults.generated_text.choices[0].message
                            .content
                        }
                      </span>
                    </div>
                  </div>
                )}
            </div>

            {/* Render search results if there are any */}
            <Tabs>
              {Object.values(parsedSearchResults).some(
                (array) => array.length > 0
              ) && (
                <div className="mt-6 pb-16">
                  <TabList>
                    {parsedSearchResults.bolts.length > 0 && <Tab>BOLTS</Tab>}
                    {parsedSearchResults.bips.length > 0 && <Tab>BIPS</Tab>}
                    {parsedSearchResults.lnd.length > 0 && <Tab>LND</Tab>}
                    {parsedSearchResults.coreln.length > 0 && <Tab>CORELN</Tab>}
                    {parsedSearchResults.rustln.length > 0 && <Tab>RUSTLN</Tab>}
                  </TabList>
                  {parsedSearchResults.bolts.length > 0 && (
                    <TabPanel>
                      <div className="my-4">
                        {parsedSearchResults.bolts.map((result, index) => (
                          <div key={index}>
                            <div className="overflow-x-auto max-w-[750px]">
                              <SyntaxHighlighter
                                language="markdown"
                                style={prism}
                              >
                                {result.page_content}
                              </SyntaxHighlighter>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabPanel>
                  )}
                  {parsedSearchResults.bips.length > 0 && (
                    <TabPanel>
                      <div className="my-4">
                        {parsedSearchResults.bips.map((result, index) => (
                          <div key={index}>
                            <div className="overflow-x-auto max-w-[750px]">
                              <SyntaxHighlighter
                                language="markdown"
                                style={prism}
                              >
                                {result.page_content}
                              </SyntaxHighlighter>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabPanel>
                  )}
                  {parsedSearchResults.lnd.length > 0 && (
                    <TabPanel>
                      <div className="my-4">
                        {parsedSearchResults.lnd.map((result, index) => (
                          <div key={index}>
                            <div className="overflow-x-auto max-w-[750px]">
                              <SyntaxHighlighter language="go" style={prism}>
                                {result.page_content}
                              </SyntaxHighlighter>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabPanel>
                  )}
                  {parsedSearchResults.coreln.length > 0 && (
                    <TabPanel>
                      <div className="my-4">
                        {parsedSearchResults.coreln.map((result, index) => (
                          <div key={index}>
                            <div className="overflow-x-auto max-w-[750px]">
                              <SyntaxHighlighter language="c" style={prism}>
                                {result.page_content}
                              </SyntaxHighlighter>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabPanel>
                  )}
                  {parsedSearchResults.rustln.length > 0 && (
                    <TabPanel>
                      <div className="my-4">
                        {parsedSearchResults.rustln.map((result, index) => (
                          <div key={index}>
                            <div className="overflow-x-auto max-w-[750px]">
                              <SyntaxHighlighter language="rust" style={prism}>
                                {result.page_content}
                              </SyntaxHighlighter>
                            </div>
                          </div>
                        ))}
                      </div>
                    </TabPanel>
                  )}
                </div>
              )}
            </Tabs>
          </div>
        </div>
        <Footer />
      </div>
    </>
  );
}
