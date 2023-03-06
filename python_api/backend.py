import os
import signal
from collections import defaultdict

import openai
from chromadb.utils import embedding_functions
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

app = Flask(__name__)
CORS(app)

FIELD_NAMES = ["bips", "bolts", "coreln", "lnd", "rustln"]


def get_similarity_for_field(query, vectorstore, field_name, k):
    return vectorstore.similarity_search_with_score(query, filter={"doc_type": {"$eq": field_name}}, k=k)


def make_chatgpt_call(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant",
             "content": messages},
        ]
    )


def get_return_dict(generated_text, docs_per_field):
    output = {}
    for field_name in FIELD_NAMES:
        output[field_name] = docs_per_field[field_name]
    output["generated_text"] = generated_text
    if len(output["coreln"]) == 0:
        output["coreln"].append({
            "lookup_index": 0,
            "lookup_str": "",
            "metadata": {
                "doc_type": "coreln",
                "filepath": "../implementations/c/core-ln/gossipd/test/run-check_channel_announcement.c",
                "length": 15184,
                "slug": "../implementations/c/core-ln/gossipd/test/run-check_channel_announcement.c"
            },
            "page_content": "../implementations/c/core-ln/gossipd/test/run-check_channel_announcement.c\n\n/* Test of https://github.com/ElementsProject/lightning/issues/3703:\n *\n * > 2020-05-04T05:17:36.958Z **BROKEN** gossipd: peer 0254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d3 invalid local_channel_announcement 0db201b3010011effc9ed10fceccfae5f9e3fef20d983b06eed030e968fd8d1e6c5905e18f9f2df6a43f00d7c0ddf52e0467ab1e32394051b72ea6343fb008a4117c265f3d7b732bab7df4ee404ac926aef6610f4eb33e31baabfd9afdbf897c8a80057efa1468362b4d2cc0a5482013e1058c8205717f85c3bc82c3ea89f17cfeac21e2cb2ac65b429f79b24fbd51094bee5e080d4c7cfc28a584e279075643054a48b2972f0b72becfd57e03297bf0102b09329982e0ac839dc120959c07456431d3c8fd1430ffe2cc2710e9600e602779c9cf5f91e95874ef4bcf9f0bdda2ce2be97bba562848a2717acdb8dec30bd5073f2f853776cc98f0b6cddc2dcfb57aa69fa7c43400030800006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d619000000000009984d00063a00010254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d303baa70886d9200af0ffbd3f9e18d96008331c858456b16e3a9b41e735c6208fef03c8731bbac446b7d11b7f5a1861c7d2c87ccf429780c74463de3428dceeb73ad702b3e55c7a1a6cdf17a83a801f7f8f698e4980323e2584f27a643a1b0519ebf8c7 (001100000000000000000000000000000000000000000000000000000000000000000463426164206e6f64655f7369676e61747572655f3120333034343032323031316566666339656431306663656363666165356639653366656632306439383362303665656430333065393638666438643165366335393035653138663966303232303264663661343366303064376330646466353265303436376162316533323339343035316237326561363334336662303038613431313763323635663364376220686173682062623932623866343562343865363561643266326366666632323432666139323162346366343666373039613337326361373738383533376538396439646531206f6e206e6f64655f616e6e6f756e63656d656e7420303130303131656666633965643130666365636366616535663965336665663230643938336230366565643033306539363866643864316536633539303565313866396632646636613433663030643763306464663532653034363761623165333233393430353162373265613633343366623030386134313137633236356633643762373332626162376466346565343034616339323661656636363130663465623333653331626161626664396166646266383937633861383030353765666131343638333632623464326363306135343832303133653130353863383230353731376638356333626338326333656138396631376366656163323165326362326163363562343239663739623234666264353130393462656535653038306434633763666332386135383465323739303735363433303534613438623239373266306237326265636664353765303332393762663031303262303933323939383265306163383339646331323039353963303734353634333164336338666431343330666665326363323731306539363030653630323737396339636635663931653935383734656634626366396630626464613263653262653937626261353632383438613237313761636462386465633330626435303733663266383533373736636339386630623663646463326463666235376161363966613763343334303030333038303030303666653238633061623666316233373263316136613234366165363366373466393331653833363565313561303839633638643631393030303030303030303030393938346430303036336130303031303235346666383038663533623266386334356537346237303433306633333663366337366261326634616632383966343864363038366165366536303436326433303362616137303838366439323030616630666662643366396531386439363030383333316338353834353662313665336139623431653733356336323038666566303363383733316262616334343662376431316237663561313836316337643263383763636634323937383063373434363364653334323864636565623733616437303262336535356337613161366364663137613833613830316637663866363938653439383033323365323538346632376136343361316230353139656266386337)\n *\n * OK, so your peer is 0254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d3, and we consider it to be a bad channel_announcement signature (it says \"node_announcement\" in the message below, but that's a typo!):\n\n```\nBad node_signature_1 3044022011effc9ed10fceccfae5f9e3fef20d983b06eed030e968fd8d1e6c5905e18f9f02202df6a43f00d7c0ddf52e0467ab1e32394051b72ea6343fb008a4117c265f3d7b hash bb92b8f45b48e65ad2f2cfff2242fa921b4cf46f709a372ca7788537e89d9de1 on node_announcement 010011effc9ed10fceccfae5f9e3fef20d983b06eed030e968fd8d1e6c5905e18f9f2df6a43f00d7c0ddf52e0467ab1e32394051b72ea6343fb008a4117c265f3d7b732bab7df4ee404ac926aef6610f4eb33e31baabfd9afdbf897c8a80057efa1468362b4d2cc0a5482013e1058c8205717f85c3bc82c3ea89f17cfeac21e2cb2ac65b429f79b24fbd51094bee5e080d4c7cfc28a584e279075643054a48b2972f0b72becfd57e03297bf0102b09329982e0ac839dc120959c07456431d3c8fd1430ffe2cc2710e9600e602779c9cf5f91e95874ef4bcf9f0bdda2ce2be97bba562848a2717acdb8dec30bd5073f2f853776cc98f0b6cddc2dcfb57aa69fa7c43400030800006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d619000000000009984d00063a00010254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d303baa70886d9200af0ffbd3f9e18d96008331c858456b16e3a9b41e735c6208fef03c8731bbac446b7d11b7f5a1861c7d2c87ccf429780c74463de3428dceeb73ad702b3e55c7a1a6cdf17a83a801f7f8f698e4980323e2584f27a643a1b0519ebf8c7\n```\n\nHere's what we think the channel_announcement should look like:\n```\nWIRE_CHANNEL_ANNOUNCEMENT:\nnode_signature_1=3044022011effc9ed10fceccfae5f9e3fef20d983b06eed030e968fd8d1e6c5905e18f9f02202df6a43f00d7c0ddf52e0467ab1e32394051b72ea6343fb008a4117c265f3d7b\nnode_signature_2=30440220732bab7df4ee404ac926aef6610f4eb33e31baabfd9afdbf897c8a80057efa14022068362b4d2cc0a5482013e1058c8205717f85c3bc82c3ea89f17cfeac21e2cb2a\nbitcoin_signature_1=3045022100c65b429f79b24fbd51094bee5e080d4c7cfc28a584e279075643054a48b2972f02200b72becfd57e03297bf0102b09329982e0ac839dc120959c07456431d3c8fd14\nbitcoin_signature_2=3044022030ffe2cc2710e9600e602779c9cf5f91e95874ef4bcf9f0bdda2ce2be97bba5602202848a2717acdb8dec30bd5073f2f853776cc98f0b6cddc2dcfb57aa69fa7c434\nfeatures=[080000]\nchain_hash=000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f\nshort_channel_id=628813x1594x1\nnode_id_1=0254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d3\nnode_id_2=03baa70886d9200af0ffbd3f9e18d96008331c858456b16e3a9b41e735c6208fef\nbitcoin_key_1=03c8731bbac446b7d11b7f5a1861c7d2c87ccf429780c74463de3428dceeb73ad7\nbitcoin_key_2=02b3e55c7a1a6cdf17a83a801f7f8f698e4980323e2584f27a643a1b0519ebf8c7\n```\n\nIn particular, we set feature bit 19.  The spec says we should set feature bit 18 (which is clearly wrong!).\n*/\n\n#include \"config.h\"\n#include \"../common/wire_error.c\"\n#include \"../routing.c\"\n#include <common/blinding.h>\n#include <common/channel_type.h>\n#include <common/ecdh.h>\n#include <common/json_stream.h>\n#include <common/onionreply.h>\n#include <common/setup.h>\n#include <stdio.h>\n\n/* AUTOGENERATED MOCKS START */\n/* Generated stub for blinding_hash_e_and_ss */\nvoid blinding_hash_e_and_ss(const struct pubkey *e UNNEEDED,\n\t\t\t    const struct secret *ss UNNEEDED,\n\t\t\t    struct sha256 *sha UNNEEDED)\n{ fprintf(stderr, \"blinding_hash_e_and_ss called!\\n\"); abort(); }\n/* Generated stub for blinding_next_privkey */\nbool blinding_next_privkey(const struct privkey *e UNNEEDED,\n\t\t\t   const struct sha256 *h UNNEEDED,\n\t\t\t   struct privkey *next UNNEEDED)\n{ fprintf(stderr, \"blinding_next_privkey called!\\n\"); abort(); }\n/* Generated stub for blinding_next_pubkey */\nbool blinding_next_pubkey(const struct pubkey *pk UNNEEDED,\n\t\t\t  const struct sha256 *h UNNEEDED,\n\t\t\t  struct pubkey *next UNNEEDED)\n{ fprintf(stderr, \"blinding_next_pubkey called!\\n\"); abort(); }\n/* Generated stub for cupdate_different */\nbool cupdate_different(struct gossip_store *gs UNNEEDED,\n\t\t       const struct half_chan *hc UNNEEDED,\n\t\t       const u8 *cupdate UNNEEDED)\n{ fprintf(stderr, \"cupdate_different called!\\n\"); abort(); }\n/* Generated stub for gossip_store_add */\nu64 gossip_store_add(struct gossip_store *gs UNNEEDED, const u8 *gossip_msg UNNEEDED,\n\t\t     u32 timestamp UNNEEDED, bool push UNNEEDED, bool zombie UNNEEDED, bool spam UNNEEDED,\n\t\t     const u8 *addendum UNNEEDED)\n{ fprintf(stderr, \"gossip_store_add called!\\n\"); abort(); }\n/* Generated stub for gossip_store_add_private_update */\nu64 gossip_store_add_private_update(struct gossip_store *gs UNNEEDED, const u8 *update UNNEEDED)\n{ fprintf(stderr, \"gossip_store_add_private_update called!\\n\"); abort(); }\n/* Generated stub for gossip_store_delete */\nvoid gossip_store_delete(struct gossip_store *gs UNNEEDED,\n\t\t\t struct broadcastable *bcast UNNEEDED,\n\t\t\t int type UNNEEDED)\n{ fprintf(stderr, \"gossip_store_delete called!\\n\"); abort(); }\n/* Generated stub for gossip_store_get */\nconst u8 *gossip_store_get(const tal_t *ctx UNNEEDED,\n\t\t\t   struct gossip_store *gs UNNEEDED,\n\t\t\t   u64 offset UNNEEDED)\n{ fprintf(stderr, \"gossip_store_get called!\\n\"); abort(); }\n/* Generated stub for gossip_store_get_private_update */\nconst u8 *gossip_store_get_private_update(const tal_t *ctx UNNEEDED,\n\t\t\t\t\t  struct gossip_store *gs UNNEEDED,\n\t\t\t\t\t  u64 offset UNNEEDED)\n{ fprintf(stderr, \"gossip_store_get_private_update called!\\n\"); abort(); }\n/* Generated stub for gossip_store_mark_channel_deleted */\nvoid gossip_store_mark_channel_deleted(struct gossip_store *gs UNNEEDED,\n\t\t\t\t       const struct short_channel_id *scid UNNEEDED)\n{ fprintf(stderr, \"gossip_store_mark_channel_deleted called!\\n\"); abort(); }\n/* Generated stub for gossip_store_mark_channel_zombie */\nvoid gossip_store_mark_channel_zombie(struct gossip_store *gs UNNEEDED,\n\t\t\t\t      struct broadcastable *bcast UNNEEDED)\n{ fprintf(stderr, \"gossip_store_mark_channel_zombie called!\\n\"); abort(); }\n/* Generated stub for gossip_store_mark_cupdate_zombie */\nvoid gossip_store_mark_cupdate_zombie(struct gossip_store *gs UNNEEDED,\n\t\t\t\t      struct broadcastable *bcast UNNEEDED)\n{ fprintf(stderr, \"gossip_store_mark_cupdate_zombie called!\\n\"); abort(); }\n/* Generated stub for gossip_store_new */\nstruct gossip_store *gossip_store_new(struct routing_state *rstate UNNEEDED,\n\t\t\t\t      struct list_head *peers UNNEEDED)\n{ fprintf(stderr, \"gossip_store_new called!\\n\"); abort(); }\n/* Generated stub for memleak_add_helper_ */\nvoid memleak_add_helper_(const tal_t *p UNNEEDED, void (*cb)(struct htable *memtable UNNEEDED,\n\t\t\t\t\t\t    const tal_t *)){ }\n/* Generated stub for memleak_scan_htable */\nvoid memleak_scan_htable(struct htable *memtable UNNEEDED, const struct htable *ht UNNEEDED)\n{ fprintf(stderr, \"memleak_scan_htable called!\\n\"); abort(); }\n/* Generated stub for memleak_scan_intmap_ */\nvoid memleak_scan_intmap_(struct htable *memtable UNNEEDED, const struct intmap *m UNNEEDED)\n{ fprintf(stderr, \"memleak_scan_intmap_ called!\\n\"); abort(); }\n/* Generated stub for nannounce_different */\nbool nannounce_different(struct gossip_store *gs UNNEEDED,\n\t\t\t const struct node *node UNNEEDED,\n\t\t\t const u8 *nannounce UNNEEDED,\n\t\t\t bool *only_missing_tlv UNNEEDED)\n{ fprintf(stderr, \"nannounce_different called!\\n\"); abort(); }\n/* Generated stub for new_reltimer_ */\nstruct oneshot *new_reltimer_(struct timers *timers UNNEEDED,\n\t\t\t      const tal_t *ctx UNNEEDED,\n\t\t\t      struct timerel expire UNNEEDED,\n\t\t\t      void (*cb)(void *) UNNEEDED, void *arg UNNEEDED)\n{ fprintf(stderr, \"new_reltimer_ called!\\n\"); abort(); }\n/* Generated stub for notleak_ */\nvoid *notleak_(void *ptr UNNEEDED, bool plus_children UNNEEDED)\n{ fprintf(stderr, \"notleak_ called!\\n\"); abort(); }\n/* Generated stub for peer_supplied_good_gossip */\nvoid peer_supplied_good_gossip(struct peer *peer UNNEEDED, size_t amount UNNEEDED)\n{ fprintf(stderr, \"peer_supplied_good_gossip called!\\n\"); abort(); }\n/* Generated stub for status_failed */\nvoid status_failed(enum status_failreason code UNNEEDED,\n\t\t   const char *fmt UNNEEDED, ...)\n{ fprintf(stderr, \"status_failed called!\\n\"); abort(); }\n/* Generated stub for status_fmt */\nvoid status_fmt(enum log_level level UNNEEDED,\n\t\tconst struct node_id *peer UNNEEDED,\n\t\tconst char *fmt UNNEEDED, ...)\n\n{ fprintf(stderr, \"status_fmt called!\\n\"); abort(); }\n/* AUTOGENERATED MOCKS END */\n\nint main(int argc, char *argv[])\n{\n\tstruct bitcoin_blkid chain_hash;\n\tu8 *features, *err;\n\tsecp256k1_ecdsa_signature node_signature_1, node_signature_2;\n\tsecp256k1_ecdsa_signature bitcoin_signature_1, bitcoin_signature_2;\n\tstruct short_channel_id short_channel_id;\n\tstruct node_id node_id_1, node_id_2;\n\tstruct pubkey bitcoin_key_1, bitcoin_key_2;\n\tconst u8 *cannounce;\n\n\tcommon_setup(argv[0]);\n\n\tcannounce = tal_hexdata(tmpctx, \"010011effc9ed10fceccfae5f9e3fef20d983b06eed030e968fd8d1e6c5905e18f9f2df6a43f00d7c0ddf52e0467ab1e32394051b72ea6343fb008a4117c265f3d7b732bab7df4ee404ac926aef6610f4eb33e31baabfd9afdbf897c8a80057efa1468362b4d2cc0a5482013e1058c8205717f85c3bc82c3ea89f17cfeac21e2cb2ac65b429f79b24fbd51094bee5e080d4c7cfc28a584e279075643054a48b2972f0b72becfd57e03297bf0102b09329982e0ac839dc120959c07456431d3c8fd1430ffe2cc2710e9600e602779c9cf5f91e95874ef4bcf9f0bdda2ce2be97bba562848a2717acdb8dec30bd5073f2f853776cc98f0b6cddc2dcfb57aa69fa7c43400030800006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d619000000000009984d00063a00010254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d303baa70886d9200af0ffbd3f9e18d96008331c858456b16e3a9b41e735c6208fef03c8731bbac446b7d11b7f5a1861c7d2c87ccf429780c74463de3428dceeb73ad702b3e55c7a1a6cdf17a83a801f7f8f698e4980323e2584f27a643a1b0519ebf8c7\", strlen(\"010011effc9ed10fceccfae5f9e3fef20d983b06eed030e968fd8d1e6c5905e18f9f2df6a43f00d7c0ddf52e0467ab1e32394051b72ea6343fb008a4117c265f3d7b732bab7df4ee404ac926aef6610f4eb33e31baabfd9afdbf897c8a80057efa1468362b4d2cc0a5482013e1058c8205717f85c3bc82c3ea89f17cfeac21e2cb2ac65b429f79b24fbd51094bee5e080d4c7cfc28a584e279075643054a48b2972f0b72becfd57e03297bf0102b09329982e0ac839dc120959c07456431d3c8fd1430ffe2cc2710e9600e602779c9cf5f91e95874ef4bcf9f0bdda2ce2be97bba562848a2717acdb8dec30bd5073f2f853776cc98f0b6cddc2dcfb57aa69fa7c43400030800006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d619000000000009984d00063a00010254ff808f53b2f8c45e74b70430f336c6c76ba2f4af289f48d6086ae6e60462d303baa70886d9200af0ffbd3f9e18d96008331c858456b16e3a9b41e735c6208fef03c8731bbac446b7d11b7f5a1861c7d2c87ccf429780c74463de3428dceeb73ad702b3e55c7a1a6cdf17a83a801f7f8f698e4980323e2584f27a643a1b0519ebf8c7\"));\n\tif (!fromwire_channel_announcement(cannounce, cannounce,\n\t\t\t\t\t   &node_signature_1,\n\t\t\t\t\t   &node_signature_2,\n\t\t\t\t\t   &bitcoin_signature_1,\n\t\t\t\t\t   &bitcoin_signature_2,\n\t\t\t\t\t   &features,\n\t\t\t\t\t   &chain_hash,\n\t\t\t\t\t   &short_channel_id,\n\t\t\t\t\t   &node_id_1,\n\t\t\t\t\t   &node_id_2,\n\t\t\t\t\t   &bitcoin_key_1,\n\t\t\t\t\t   &bitcoin_key_2))\n\t\tabort();\n\n\terr = check_channel_announcement(cannounce,\n\t\t\t\t\t &node_id_1, &node_id_2,\n\t\t\t\t\t &bitcoin_key_1, &bitcoin_key_2,\n\t\t\t\t\t &node_signature_1, &node_signature_2,\n\t\t\t\t\t &bitcoin_signature_1,\n\t\t\t\t\t &bitcoin_signature_2,\n\t\t\t\t\t cannounce);\n\tassert(err);\n\tassert(memmem(err, tal_bytelen(err),\n\t\t      \"Bad node_signature_1\", strlen(\"Bad node_signature_1\")));\n\n\t/* Turns out they didn't include the feature bit at all. */\n\tcannounce = towire_channel_announcement(tmpctx,\n\t\t\t\t\t\t&node_signature_1,\n\t\t\t\t\t\t&node_signature_2,\n\t\t\t\t\t\t&bitcoin_signature_1,\n\t\t\t\t\t\t&bitcoin_signature_2,\n\t\t\t\t\t\tNULL,\n\t\t\t\t\t\t&chain_hash,\n\t\t\t\t\t\t&short_channel_id,\n\t\t\t\t\t\t&node_id_1,\n\t\t\t\t\t\t&node_id_2,\n\t\t\t\t\t\t&bitcoin_key_1,\n\t\t\t\t\t\t&bitcoin_key_2);\n\terr = check_channel_announcement(cannounce,\n\t\t\t\t\t &node_id_1, &node_id_2,\n\t\t\t\t\t &bitcoin_key_1, &bitcoin_key_2,\n\t\t\t\t\t &node_signature_1, &node_signature_2,\n\t\t\t\t\t &bitcoin_signature_1,\n\t\t\t\t\t &bitcoin_signature_2,\n\t\t\t\t\t cannounce);\n\tassert(err);\n\tassert(memmem(err, tal_bytelen(err),\n\t\t      \"Bad node_signature_2\", strlen(\"Bad node_signature_2\")));\n\n\tcommon_shutdown();\n\treturn 0;\n}\n"
        })
    if len(output["rustln"]) == 0:
        output["rustln"].append(
            {
                "lookup_index": 0,
                "lookup_str": "",
                "metadata": {
                    "doc_type": "rustln",
                    "filepath": "../implementations/rust/rust-lightning/lightning/src/ln/priv_short_conf_tests.rs",
                    "length": 1772,
                    "slug": "fn test_connect_before_funding() {"
                },
                "page_content": "fn test_connect_before_funding() {\n\nfn test_connect_before_funding() {\n\t// Tests for a particularly dumb explicit panic that existed prior to 0.0.111 for 0conf\n\t// channels. If we received a block while awaiting funding for 0-conf channels we'd hit an\n\t// explicit panic when deciding if we should broadcast our channel_ready message.\n\tlet chanmon_cfgs = create_chanmon_cfgs(2);\n\tlet node_cfgs = create_node_cfgs(2, &chanmon_cfgs);\n\n\tlet mut manually_accept_conf = test_default_channel_config();\n\tmanually_accept_conf.manually_accept_inbound_channels = true;\n\n\tlet node_chanmgrs = create_node_chanmgrs(2, &node_cfgs, &[None, Some(manually_accept_conf)]);\n\tlet nodes = create_network(2, &node_cfgs, &node_chanmgrs);\n\n\tnodes[0].node.create_channel(nodes[1].node.get_our_node_id(), 100_000, 10_001, 42, None).unwrap();\n\tlet open_channel = get_event_msg!(nodes[0], MessageSendEvent::SendOpenChannel, nodes[1].node.get_our_node_id());\n\n\tnodes[1].node.handle_open_channel(&nodes[0].node.get_our_node_id(), &open_channel);\n\tlet events = nodes[1].node.get_and_clear_pending_events();\n\tassert_eq!(events.len(), 1);\n\tmatch events[0] {\n\t\tEvent::OpenChannelRequest { temporary_channel_id, .. } => {\n\t\t\tnodes[1].node.accept_inbound_channel_from_trusted_peer_0conf(&temporary_channel_id, &nodes[0].node.get_our_node_id(), 0).unwrap();\n\t\t},\n\t\t_ => panic!(\"Unexpected event\"),\n\t};\n\n\tlet mut accept_channel = get_event_msg!(nodes[1], MessageSendEvent::SendAcceptChannel, nodes[0].node.get_our_node_id());\n\tassert_eq!(accept_channel.minimum_depth, 0);\n\tnodes[0].node.handle_accept_channel(&nodes[1].node.get_our_node_id(), &accept_channel);\n\n\tlet events = nodes[0].node.get_and_clear_pending_events();\n\tassert_eq!(events.len(), 1);\n\tmatch events[0] {\n\t\tEvent::FundingGenerationReady { .. } => {},\n\t\t_ => panic!(\"Unexpected event\"),\n\t}\n\n\tconnect_blocks(&nodes[0], 1);\n\tconnect_blocks(&nodes[1], 1);\n}\n"
            })
    if len(output["lnd"]) == 0:
        output["lnd"].append({
            "lookup_index": 0,
            "lookup_str": "",
            "metadata": {
                "doc_type": "lnd",
                "filepath": "../implementations/go/lnd/channeldb/payment_control_test.go",
                "length": 2277,
                "slug": "func createTestPayments(t *testing.T, p *PaymentControl, payments []*payment) {"
            },
            "page_content": "func createTestPayments(t *testing.T, p *PaymentControl, payments []*payment) {\n\nfunc createTestPayments(t *testing.T, p *PaymentControl, payments []*payment) {\n\tattemptID := uint64(0)\n\n\tfor i := 0; i < len(payments); i++ {\n\t\tinfo, attempt, preimg, err := genInfo()\n\t\trequire.NoError(t, err, \"unable to generate htlc message\")\n\n\t\t// Set the payment id accordingly in the payments slice.\n\t\tpayments[i].id = info.PaymentIdentifier\n\n\t\tattempt.AttemptID = attemptID\n\t\tattemptID++\n\n\t\t// Init the payment.\n\t\terr = p.InitPayment(info.PaymentIdentifier, info)\n\t\trequire.NoError(t, err, \"unable to send htlc message\")\n\n\t\t// Register and fail the first attempt for all payments.\n\t\t_, err = p.RegisterAttempt(info.PaymentIdentifier, attempt)\n\t\trequire.NoError(t, err, \"unable to send htlc message\")\n\n\t\thtlcFailure := HTLCFailUnreadable\n\t\t_, err = p.FailAttempt(\n\t\t\tinfo.PaymentIdentifier, attempt.AttemptID,\n\t\t\t&HTLCFailInfo{\n\t\t\t\tReason: htlcFailure,\n\t\t\t},\n\t\t)\n\t\trequire.NoError(t, err, \"unable to fail htlc\")\n\n\t\t// Increase the HTLC counter in the payments slice for the\n\t\t// failed attempt.\n\t\tpayments[i].htlcs++\n\n\t\t// Depending on the test case, fail or succeed the next\n\t\t// attempt.\n\t\tattempt.AttemptID = attemptID\n\t\tattemptID++\n\n\t\t_, err = p.RegisterAttempt(info.PaymentIdentifier, attempt)\n\t\trequire.NoError(t, err, \"unable to send htlc message\")\n\n\t\tswitch payments[i].status {\n\t\t// Fail the attempt and the payment overall.\n\t\tcase StatusFailed:\n\t\t\thtlcFailure := HTLCFailUnreadable\n\t\t\t_, err = p.FailAttempt(\n\t\t\t\tinfo.PaymentIdentifier, attempt.AttemptID,\n\t\t\t\t&HTLCFailInfo{\n\t\t\t\t\tReason: htlcFailure,\n\t\t\t\t},\n\t\t\t)\n\t\t\trequire.NoError(t, err, \"unable to fail htlc\")\n\n\t\t\tfailReason := FailureReasonNoRoute\n\t\t\t_, err = p.Fail(info.PaymentIdentifier,\n\t\t\t\tfailReason)\n\t\t\trequire.NoError(t, err, \"unable to fail payment hash\")\n\n\t\t// Settle the attempt\n\t\tcase StatusSucceeded:\n\t\t\t_, err := p.SettleAttempt(\n\t\t\t\tinfo.PaymentIdentifier, attempt.AttemptID,\n\t\t\t\t&HTLCSettleInfo{\n\t\t\t\t\tPreimage: preimg,\n\t\t\t\t},\n\t\t\t)\n\t\t\trequire.NoError(t, err, \"no error should have been \"+\n\t\t\t\t\"received from settling a htlc attempt\")\n\n\t\t// We leave the attempt in-flight by doing nothing.\n\t\tcase StatusInFlight:\n\t\t}\n\n\t\t// Increase the HTLC counter in the payments slice for any\n\t\t// attempt above.\n\t\tpayments[i].htlcs++\n\t}\n}\n\n// assertPayments is a helper function that given a slice of payment and\n// indices for the slice asserts that exactly the same payments in the\n// slice for the provided indices exist when fetching payments from the\n// database."
        })
    if len(output["bolts"]) == 0:
        output["bolts"].append({
            "lookup_index": 0,
            "lookup_str": "",
            "metadata": {
                "filepath": "bolts/07-routing-gossip.md",
                "length": 1690,
                "tokens": 205
            },
            "page_content": "The `channel_announcement` Message\n\nThis gossip message contains ownership information regarding a channel. It ties\neach on-chain Bitcoin key to the associated Lightning node key, and vice-versa.\nThe channel is not practically usable until at least one side has announced\nits fee levels and expiry, using `channel_update`.\n\nProving the existence of a channel between `node_1` and `node_2` requires:\n\n1. proving that the funding transaction pays to `bitcoin_key_1` and\n`bitcoin_key_2`\n2. proving that `node_1` owns `bitcoin_key_1`\n3. proving that `node_2` owns `bitcoin_key_2`\n\nAssuming that all nodes know the unspent transaction outputs, the first proof is\naccomplished by a node finding the output given by the `short_channel_id` and\nverifying that it is indeed a P2WSH funding transaction output for those keys\nspecified in [BOLT #3](03-transactions.md#funding-transaction-output).\n\nThe last two proofs are accomplished through explicit signatures:\n`bitcoin_signature_1` and `bitcoin_signature_2` are generated for each\n`bitcoin_key` and each of the corresponding `node_id`s are signed.\n\nIt's also necessary to prove that `node_1` and `node_2` both agree on the\nannouncement message: this is accomplished by having a signature from each\n`node_id` (`node_signature_1` and `node_signature_2`) signing the message.\n\n1. type: 256 (`channel_announcement`)\n2. data:\n* [`signature`:`node_signature_1`]\n* [`signature`:`node_signature_2`]\n* [`signature`:`bitcoin_signature_1`]\n* [`signature`:`bitcoin_signature_2`]\n* [`u16`:`len`]\n* [`len*byte`:`features`]\n* [`chain_hash`:`chain_hash`]\n* [`short_channel_id`:`short_channel_id`]\n* [`point`:`node_id_1`]\n* [`point`:`node_id_2`]\n* [`point`:`bitcoin_key_1`]\n* [`point`:`bitcoin_key_2`]"
        })
    return output


def determine_doc_type(filepath):
    if "/lnd" in filepath:
        return "lnd"
    elif "/rust-lightning" in filepath:
        return "rustln"
    elif "/core-ln" in filepath:
        return "coreln"
    elif filepath.startswith("bips"):
        return "bip"
    elif filepath.startswith("bolt"):
        return "bolts"
    else:
        raise Exception("Unknown doc type")


@app.route("/similarity_search", methods=["GET"])
def similarity_search():
    query = request.args.get("query")
    if query is None:
        return jsonify({"error": "Query parameter is required"}), 400
    print("Received request: ", query)
    docs_per_field = defaultdict(list)
    try:
        k = 10
        docs = vectorstore.similarity_search_with_score(query, k)
        if not docs:
            return jsonify({"error": "No documents found"}), 404
        from pprint import pprint
        pprint(docs)
        for doc in docs:
            doc_type = determine_doc_type(
                doc[0].dict()["metadata"]["filepath"])
            docs_per_field[doc_type].append(doc[0].dict())

        # for field_name in FIELD_NAMES:
        #     k = 4
        #     docs = get_similarity_for_field(query, vectorstore, field_name, k)
        #     print("through vectorstore")
        #     if not docs:
        #         return jsonify({"error": "No documents found"}), 404
        #     # docs_per_field[field_name].append((docs[0].dict(), docs[1]))
        #     docs_per_field[field_name] = [doc[0].dict() for doc in docs]

        generated_text = make_chatgpt_call(query)

        # Return the lists as JSON
        return jsonify(get_return_dict(generated_text, docs_per_field))

    except Exception as e:
        print("Error in similarity search:", e)
        return jsonify({"error": "Internal server error"}), 500


openai_ef = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Chroma(collection_name="bitcoin",
                     embedding_function=openai_ef,
                     persist_directory="/Users/kodylow/Documents/github/deep-learning/ln-spec-bot/chromadb_builder/dbs")


print("Starting server on port 4080")
app.run(host="0.0.0.0", port=4080)
