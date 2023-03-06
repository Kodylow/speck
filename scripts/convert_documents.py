def convert_document_to_json(document):
    return {
        "lookup_index": document.lookup_index,
        "lookup_str": document.lookup_str,
        "metadata": {
            "Author": document.metadata["Author"],
            "BIP": document.metadata["BIP"],
            "Comments-Summary": document.metadata["Comments-Summary"],
            "Comments-URI": document.metadata["Comments-URI"],
            "Created": document.metadata["Created"],
            "Layer": document.metadata["Layer"],
            "License": document.metadata["License"],
            "Status": document.metadata["Status"],
            "Title": document.metadata["Title"],
            "Type": document.metadata["Type"],
            "filepath": document.metadata["filepath"],
            "length": document.metadata["length"],
            "tokens": document.metadata["tokens"],
        },
        "page_content": document.page_content,
    }


def convert_documents_to_json(documents):
    return [convert_document_to_json(document[0]) for document in documents]


docs = [{
    "lookup_index": 0,
    "lookup_str": "",
    "metadata": {
        "Author": "Christian Decker decker.christian@gmail.com",
        "BIP": "118",
        "Comments-Summary": "No comments yet.",
        "Comments-URI": "https://github.com/bitcoin/bips/wiki/Comments:BIP-0118",
        "Created": "2017-02-28",
        "Layer": "Consensus (soft fork)",
        "License": "BSD-3-Clause",
        "Status": "Draft",
        "Title": "SIGHASH_ANYPREVOUT for Taproot Scripts",
        "Type": "Standards Track",
        "Requires": "340, 341, 342",
        "filepath": "bips/bip-0118.mediawiki",
        "length": 4420,
        "tokens": 666
    },
    "page_content": "Public key {#public_key}\n\nTo convert the 1-byte BIP 118 public key for use with [BIP\n340](bip-0340.mediawiki 'wikilink'), use the 32-byte taproot internal\nkey, p, as defined in [BIP 341](bip-0341.mediawiki 'wikilink').\n\nTo convert a 33-byte BIP 118 public key for use with [BIP\n340](bip-0340.mediawiki 'wikilink'), remove the 0x01 prefix and use\nthe remaining 32 bytes."
}, {
    "lookup_index": 0,
    "lookup_str": "",
    "metadata": {
        "Author": "Shinobius quantumedusa@gmail.com",
        "BIP": "343",
        "Comments-Summary": "No comments yet.",
        "Comments-URI": "https://github.com/bitcoin/bips/wiki/Comments:BIP-0343",
        "Created": "2021-04-25",
        "Layer": "Consensus (soft fork)",
        "License": "BSD-3-Clause",
        "Status": "Final",
        "Title": "Mandatory activation of taproot deployment",
        "Type": "Standards Track",
        "filepath": "bips/bip-0343.mediawiki",
        "length": 87,
        "tokens": 14
    },
    "page_content": "Abstract\n\nThis document specifies a BIP8 (LOT=true) deployment to activate\ntaproot."
}
]