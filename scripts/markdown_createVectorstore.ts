import fs from "fs";
import glob from "glob";
import { OpenAIEmbeddings } from "langchain/embeddings";
import { CharacterTextSplitter } from "langchain/text_splitter";
import { HNSWLib } from "langchain/vectorstores";

const dirs = ["../bips", "../bolts"];

for (const dir of dirs) {
  const data = [];
  const files: string[] = await new Promise((resolve, reject) =>
    glob(
      `${dir}/**/*.md`,
      (err: any, files: string[] | PromiseLike<string[]>) =>
        err ? reject(err) : resolve(files)
    )
  );

  for (const file of files) {
    data.push(fs.readFileSync(file, "utf-8"));
  }

  console.log(
    `Added ${files.length} files from ${dir} to data.  Splitting text into chunks...`
  );

  const textSplitter = new CharacterTextSplitter({
    chunkSize: 2000,
    separator: "\n",
  });

  let docs: any[] = [];
  for (const d of data) {
    const docOutput = textSplitter.splitText(d);
    docs = [...docs, ...docOutput];
  }

  console.log(`Initializing Store for ${dir}...`);

  const store = await HNSWLib.fromTexts(
    docs,
    docs.map((_, i) => ({ id: i })),
    new OpenAIEmbeddings()
  );

  console.clear();
  console.log(`Saving Vectorstore for ${dir}`);

  fs.mkdirSync("../vectorStores", { recursive: true });
  store.save(`../vectorStores/${dir.slice(3)}VectorStore.json`);

  console.clear();
  console.log(`VectorStore for ${dir} saved`);
}
