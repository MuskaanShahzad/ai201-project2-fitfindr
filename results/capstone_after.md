# Capstone run log: after

- Produced by: `run_capstone.py` (`one_run`), scoring as worded in `criteria.md`
- Servers: `serve.py` with the cache off; `logs/runs.jsonl` is written by `runlog.py::run_logged`
- When: 2026-11-11 20:54
- Runs: 3, with the whole test repeated each time and nothing changed in between

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A matching query completes | at least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. An impossible query stops before any model call | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Every kind of request leaves one complete log line | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. A warm matching request takes 5.0 s or less | at least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. One matching run uses 600 tokens or fewer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

A criterion is MET only if every run reaches its target.

## Run 1

- server A rate-limit pauses: 0, timeout retries: 0
- server C rate-limit pauses: 0, timeout retries: 0

### 1. A matching query completes

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:49:00+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Got the absolute ultimate Y2K butterfly baby tee for only $18 over on my depop. Honestly living out my 2000s pop star dreams with this one. Throwing it on with baggy denim and chunky sneakers for the easiest off-duty look ever.", "selected_item_id": "lst_002", "latency_s": 2.72, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 105}
{"timestamp": "2026-11-12T02:49:02+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Obsessed with this 90s navy and white track jacket to channel total retro athletic streetwear energy. Snagged it on Poshmark for $45 and honestly I'm never taking it off. Throwing it on over a white ribbed tank and baggy jeans is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.51, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 134}
{"timestamp": "2026-11-12T02:49:05+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It has that ultimate 90s model-off-duty vibe when you throw it on over a white tank and baggy dark jeans. Honestly the easiest way to pull off double denim without trying too hard.", "selected_item_id": "lst_007", "latency_s": 2.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 376, "output_tokens": 128}
{"timestamp": "2026-11-12T02:49:08+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for $48 and my Y2K streetwear dreams are officially complete. They are literally begging to be worn with a vintage denim jacket and baggy dark wash jeans. Can’t wait to stomp around in these all fall!", "selected_item_id": "lst_019", "latency_s": 2.43, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 123}
{"timestamp": "2026-11-12T02:49:10+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally caved and added this 90s floral silk midi to my depop after convincing myself I didn't need another slip dress. It was an absolute steal at $30 and the print is just too good. Obsessed with throwing an oversized grey crewneck and combat boots over it for the ultimate grunge moment. ✨", "selected_item_id": "lst_013", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 125}
```

### 2. An impossible query stops before any model call

- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:49:11+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.18, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:49:13+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.16, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:49:14+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.11, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:49:15+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.16, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:49:16+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.15, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 3. Every kind of request leaves one complete log line

- PASS (expected `ok`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS (expected `ok`): `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS (expected `no_results`): `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS (expected `rejected`): `` -> HTTP 400, 1 new log line(s)
- PASS (expected `model_unavailable`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:49:52+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Living out my 2000s pop star dreams in this butterfly tee. Grabbed it on Depop for just $18 and honestly, it’s the ultimate zero-effort fit paired with my favorite baggy jeans and chunky sneakers. Total Y2K mall rat energy. ✨🦋", "selected_item_id": "lst_002", "latency_s": 5.07, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 366, "output_tokens": 109}
{"timestamp": "2026-11-12T02:49:55+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Still not over finding this 90s navy and white striped track jacket. Snagged it on Poshmark for $45 and it’s giving major sporty-retro streetwear vibes. Throwing it over a ribbed tank and baggy jeans and I’m officially set for fall.", "selected_item_id": "lst_004", "latency_s": 2.77, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 382, "output_tokens": 122}
{"timestamp": "2026-11-12T02:49:56+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.21, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:49:56+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:50:00+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 3.62, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 4. A warm matching request takes 5.0 s or less

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:49:00+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Got the absolute ultimate Y2K butterfly baby tee for only $18 over on my depop. Honestly living out my 2000s pop star dreams with this one. Throwing it on with baggy denim and chunky sneakers for the easiest off-duty look ever.", "selected_item_id": "lst_002", "latency_s": 2.72, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 105}
{"timestamp": "2026-11-12T02:49:02+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Obsessed with this 90s navy and white track jacket to channel total retro athletic streetwear energy. Snagged it on Poshmark for $45 and honestly I'm never taking it off. Throwing it on over a white ribbed tank and baggy jeans is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.51, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 134}
{"timestamp": "2026-11-12T02:49:05+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It has that ultimate 90s model-off-duty vibe when you throw it on over a white tank and baggy dark jeans. Honestly the easiest way to pull off double denim without trying too hard.", "selected_item_id": "lst_007", "latency_s": 2.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 376, "output_tokens": 128}
{"timestamp": "2026-11-12T02:49:08+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for $48 and my Y2K streetwear dreams are officially complete. They are literally begging to be worn with a vintage denim jacket and baggy dark wash jeans. Can’t wait to stomp around in these all fall!", "selected_item_id": "lst_019", "latency_s": 2.43, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 123}
{"timestamp": "2026-11-12T02:49:10+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally caved and added this 90s floral silk midi to my depop after convincing myself I didn't need another slip dress. It was an absolute steal at $30 and the print is just too good. Obsessed with throwing an oversized grey crewneck and combat boots over it for the ultimate grunge moment. ✨", "selected_item_id": "lst_013", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 125}
```

### 5. One matching run uses 600 tokens or fewer

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:49:00+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Got the absolute ultimate Y2K butterfly baby tee for only $18 over on my depop. Honestly living out my 2000s pop star dreams with this one. Throwing it on with baggy denim and chunky sneakers for the easiest off-duty look ever.", "selected_item_id": "lst_002", "latency_s": 2.72, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 105}
{"timestamp": "2026-11-12T02:49:02+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Obsessed with this 90s navy and white track jacket to channel total retro athletic streetwear energy. Snagged it on Poshmark for $45 and honestly I'm never taking it off. Throwing it on over a white ribbed tank and baggy jeans is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.51, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 134}
{"timestamp": "2026-11-12T02:49:05+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It has that ultimate 90s model-off-duty vibe when you throw it on over a white tank and baggy dark jeans. Honestly the easiest way to pull off double denim without trying too hard.", "selected_item_id": "lst_007", "latency_s": 2.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 376, "output_tokens": 128}
{"timestamp": "2026-11-12T02:49:08+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for $48 and my Y2K streetwear dreams are officially complete. They are literally begging to be worn with a vintage denim jacket and baggy dark wash jeans. Can’t wait to stomp around in these all fall!", "selected_item_id": "lst_019", "latency_s": 2.43, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 123}
{"timestamp": "2026-11-12T02:49:10+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally caved and added this 90s floral silk midi to my depop after convincing myself I didn't need another slip dress. It was an absolute steal at $30 and the print is just too good. Obsessed with throwing an oversized grey crewneck and combat boots over it for the ultimate grunge moment. ✨", "selected_item_id": "lst_013", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 125}
```

## Run 2

- server A rate-limit pauses: 0, timeout retries: 0
- server C rate-limit pauses: 0, timeout retries: 0

### 1. A matching query completes

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:51:09+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Live, laugh, love a butterfly baby tee. Grabbed this exact Y2K dream off Depop for just $18 and I’m already living out my ultimate early 2000s pop star fantasy. Pair it with baggy dark wash jeans and chunky sneakers for the absolute best high-contrast fit.", "selected_item_id": "lst_002", "latency_s": 2.44, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 119}
{"timestamp": "2026-11-12T02:51:12+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Literal heart eyes for this 90s navy and white track jacket. Styled it over a ribbed tank and baggy denim for the ultimate sporty streetwear look, but it works just as well with chunky boots. Grabbed it on Poshmark for $45 and I'm never taking it off.", "selected_item_id": "lst_004", "latency_s": 2.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 130}
{"timestamp": "2026-11-12T02:51:14+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Scored this vintage cropped denim jacket on Poshmark for $42 and I'm obsessed with the wash. Threw it on with wide-leg khakis and a white tank for that effortless streetwear look. Honestly, it's about to be my daily uniform.", "selected_item_id": "lst_007", "latency_s": 2.6, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 354, "output_tokens": 99}
{"timestamp": "2026-11-12T02:51:17+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for $48 and I am officially in my Bratz doll era. They are giving heavy Y2K streetwear energy, especially paired with baggy dark wash denim and a vintage jacket. Can't wait to run these into the ground. 👟✨", "selected_item_id": "lst_019", "latency_s": 2.68, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 374, "output_tokens": 123}
{"timestamp": "2026-11-12T02:51:19+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Found my dream 90s floral midi slip dress and honestly I'm never taking it off. Grabbed it on Depop for just $30 and the grunge styling potential is endless. I'm obsessed with throwing an oversized grey crewneck and combat boots right over it for that ultimate 90s contrast.", "selected_item_id": "lst_013", "latency_s": 2.35, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 378, "output_tokens": 117}
```

### 2. An impossible query stops before any model call

- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:51:21+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.66, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:51:22+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.4, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:51:24+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.5, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:51:26+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 2.07, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:51:27+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.52, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 3. Every kind of request leaves one complete log line

- PASS (expected `ok`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS (expected `ok`): `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS (expected `no_results`): `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS (expected `rejected`): `` -> HTTP 400, 1 new log line(s)
- PASS (expected `model_unavailable`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:52:05+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Live, laugh, love a 2000s butterfly tee. Snagged this pastel dream on Depop for just $18 and I’m literally never taking it off. Pair it with baggy dark wash denim and chunky sneakers for the ultimate off-duty bratz doll energy. ✨🦋", "selected_item_id": "lst_002", "latency_s": 6.15, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 370, "output_tokens": 115}
{"timestamp": "2026-11-12T02:52:07+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Okay but this 90s navy and white track jacket is the ultimate sporty streetwear find. I scored it for $45 over on Poshmark and I’m literally obsessed. Throw it on with a white ribbed tank, baggy denim, and chunky sneakers for the easiest off-duty fit.", "selected_item_id": "lst_004", "latency_s": 2.33, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 127}
{"timestamp": "2026-11-12T02:52:08+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.26, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:52:08+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:52:14+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 4.69, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 4. A warm matching request takes 5.0 s or less

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:51:09+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Live, laugh, love a butterfly baby tee. Grabbed this exact Y2K dream off Depop for just $18 and I’m already living out my ultimate early 2000s pop star fantasy. Pair it with baggy dark wash jeans and chunky sneakers for the absolute best high-contrast fit.", "selected_item_id": "lst_002", "latency_s": 2.44, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 119}
{"timestamp": "2026-11-12T02:51:12+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Literal heart eyes for this 90s navy and white track jacket. Styled it over a ribbed tank and baggy denim for the ultimate sporty streetwear look, but it works just as well with chunky boots. Grabbed it on Poshmark for $45 and I'm never taking it off.", "selected_item_id": "lst_004", "latency_s": 2.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 130}
{"timestamp": "2026-11-12T02:51:14+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Scored this vintage cropped denim jacket on Poshmark for $42 and I'm obsessed with the wash. Threw it on with wide-leg khakis and a white tank for that effortless streetwear look. Honestly, it's about to be my daily uniform.", "selected_item_id": "lst_007", "latency_s": 2.6, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 354, "output_tokens": 99}
{"timestamp": "2026-11-12T02:51:17+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for $48 and I am officially in my Bratz doll era. They are giving heavy Y2K streetwear energy, especially paired with baggy dark wash denim and a vintage jacket. Can't wait to run these into the ground. 👟✨", "selected_item_id": "lst_019", "latency_s": 2.68, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 374, "output_tokens": 123}
{"timestamp": "2026-11-12T02:51:19+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Found my dream 90s floral midi slip dress and honestly I'm never taking it off. Grabbed it on Depop for just $30 and the grunge styling potential is endless. I'm obsessed with throwing an oversized grey crewneck and combat boots right over it for that ultimate 90s contrast.", "selected_item_id": "lst_013", "latency_s": 2.35, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 378, "output_tokens": 117}
```

### 5. One matching run uses 600 tokens or fewer

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:51:09+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Live, laugh, love a butterfly baby tee. Grabbed this exact Y2K dream off Depop for just $18 and I’m already living out my ultimate early 2000s pop star fantasy. Pair it with baggy dark wash jeans and chunky sneakers for the absolute best high-contrast fit.", "selected_item_id": "lst_002", "latency_s": 2.44, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 119}
{"timestamp": "2026-11-12T02:51:12+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Literal heart eyes for this 90s navy and white track jacket. Styled it over a ribbed tank and baggy denim for the ultimate sporty streetwear look, but it works just as well with chunky boots. Grabbed it on Poshmark for $45 and I'm never taking it off.", "selected_item_id": "lst_004", "latency_s": 2.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 130}
{"timestamp": "2026-11-12T02:51:14+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Scored this vintage cropped denim jacket on Poshmark for $42 and I'm obsessed with the wash. Threw it on with wide-leg khakis and a white tank for that effortless streetwear look. Honestly, it's about to be my daily uniform.", "selected_item_id": "lst_007", "latency_s": 2.6, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 354, "output_tokens": 99}
{"timestamp": "2026-11-12T02:51:17+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for $48 and I am officially in my Bratz doll era. They are giving heavy Y2K streetwear energy, especially paired with baggy dark wash denim and a vintage jacket. Can't wait to run these into the ground. 👟✨", "selected_item_id": "lst_019", "latency_s": 2.68, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 374, "output_tokens": 123}
{"timestamp": "2026-11-12T02:51:19+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Found my dream 90s floral midi slip dress and honestly I'm never taking it off. Grabbed it on Depop for just $30 and the grunge styling potential is endless. I'm obsessed with throwing an oversized grey crewneck and combat boots right over it for that ultimate 90s contrast.", "selected_item_id": "lst_013", "latency_s": 2.35, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 378, "output_tokens": 117}
```

## Run 3

- server A rate-limit pauses: 0, timeout retries: 0
- server C rate-limit pauses: 0, timeout retries: 0

### 1. A matching query completes

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:53:24+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Living out my inner 2000s pop star dreams in this butterfly baby tee. Found it on Depop for just $18 and it’s giving major nostalgia. Paired it with baggy denim and sneakers for the ultimate low-effort, high-impact fit. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.48, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 368, "output_tokens": 110}
{"timestamp": "2026-11-12T02:53:27+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found my ultimate 90s sporty aesthetic. Score this navy and white striped track jacket over on my Poshmark for just $45. It’s giving effortless retro streetwear whether you throw it on with baggy denim or wide-leg trousers!", "selected_item_id": "lst_004", "latency_s": 2.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 391, "output_tokens": 123}
{"timestamp": "2026-11-12T02:53:30+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Found my new go-to spring layer on Poshmark for $42 and I am obsessed. Obsessed with the fit of this cropped light wash, especially paired with wide-leg trousers and chunky sneakers for that effortless streetwear vibe. Runs in my closet starting today!", "selected_item_id": "lst_007", "latency_s": 2.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 355, "output_tokens": 99}
{"timestamp": "2026-11-12T02:53:33+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Found my new absolute go-to sneakers on Poshmark for $48 and I am never taking them off. They give the ultimate 90s streetwear vibe when I wear them with baggy denim and a vintage jacket. Such a good score!", "selected_item_id": "lst_019", "latency_s": 2.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 376, "output_tokens": 115}
{"timestamp": "2026-11-12T02:53:37+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement for this 90s floral silk midi. Paired it with chunky sneakers and a zip hoodie for that ultimate grunge-meets-feminine moment, but it’s just as good with a denim jacket and combat boots. Grabbed it for $30 and she’s officially live on my Depop! 🥀✨", "selected_item_id": "lst_013", "latency_s": 3.63, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 397, "output_tokens": 142}
```

### 2. An impossible query stops before any model call

- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:53:39+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.96, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:53:42+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 3.32, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:53:44+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.77, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:53:46+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.88, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:53:47+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.53, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 3. Every kind of request leaves one complete log line

- PASS (expected `ok`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS (expected `ok`): `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS (expected `no_results`): `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS (expected `rejected`): `` -> HTTP 400, 1 new log line(s)
- PASS (expected `model_unavailable`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:54:25+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Living out my ultimate 2000s pop star dreams in this butterfly baby tee. Grabbed it on Depop for just $18 and honestly, the Y2K mall-goth nostalgia is unmatched. Pair it with baggy jeans and chunky sneakers for the full off-duty look!", "selected_item_id": "lst_002", "latency_s": 6.83, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 393, "output_tokens": 137}
{"timestamp": "2026-11-12T02:54:30+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece for my closet rotation. Scored this navy and white striped track jacket for $45 over on Poshmark, and the vintage vibe is immaculate. Throwing it on over a ribbed tank and baggy denim is about to be my new everyday uniform. 🏃💨✨", "selected_item_id": "lst_004", "latency_s": 4.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 382, "output_tokens": 127}
{"timestamp": "2026-11-12T02:54:33+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 3.46, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:54:33+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:54:41+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 6.22, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 4. A warm matching request takes 5.0 s or less

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:53:24+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Living out my inner 2000s pop star dreams in this butterfly baby tee. Found it on Depop for just $18 and it’s giving major nostalgia. Paired it with baggy denim and sneakers for the ultimate low-effort, high-impact fit. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.48, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 368, "output_tokens": 110}
{"timestamp": "2026-11-12T02:53:27+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found my ultimate 90s sporty aesthetic. Score this navy and white striped track jacket over on my Poshmark for just $45. It’s giving effortless retro streetwear whether you throw it on with baggy denim or wide-leg trousers!", "selected_item_id": "lst_004", "latency_s": 2.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 391, "output_tokens": 123}
{"timestamp": "2026-11-12T02:53:30+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Found my new go-to spring layer on Poshmark for $42 and I am obsessed. Obsessed with the fit of this cropped light wash, especially paired with wide-leg trousers and chunky sneakers for that effortless streetwear vibe. Runs in my closet starting today!", "selected_item_id": "lst_007", "latency_s": 2.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 355, "output_tokens": 99}
{"timestamp": "2026-11-12T02:53:33+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Found my new absolute go-to sneakers on Poshmark for $48 and I am never taking them off. They give the ultimate 90s streetwear vibe when I wear them with baggy denim and a vintage jacket. Such a good score!", "selected_item_id": "lst_019", "latency_s": 2.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 376, "output_tokens": 115}
{"timestamp": "2026-11-12T02:53:37+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement for this 90s floral silk midi. Paired it with chunky sneakers and a zip hoodie for that ultimate grunge-meets-feminine moment, but it’s just as good with a denim jacket and combat boots. Grabbed it for $30 and she’s officially live on my Depop! 🥀✨", "selected_item_id": "lst_013", "latency_s": 3.63, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 397, "output_tokens": 142}
```

### 5. One matching run uses 600 tokens or fewer

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:53:24+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Living out my inner 2000s pop star dreams in this butterfly baby tee. Found it on Depop for just $18 and it’s giving major nostalgia. Paired it with baggy denim and sneakers for the ultimate low-effort, high-impact fit. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.48, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 368, "output_tokens": 110}
{"timestamp": "2026-11-12T02:53:27+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found my ultimate 90s sporty aesthetic. Score this navy and white striped track jacket over on my Poshmark for just $45. It’s giving effortless retro streetwear whether you throw it on with baggy denim or wide-leg trousers!", "selected_item_id": "lst_004", "latency_s": 2.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 391, "output_tokens": 123}
{"timestamp": "2026-11-12T02:53:30+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Found my new go-to spring layer on Poshmark for $42 and I am obsessed. Obsessed with the fit of this cropped light wash, especially paired with wide-leg trousers and chunky sneakers for that effortless streetwear vibe. Runs in my closet starting today!", "selected_item_id": "lst_007", "latency_s": 2.9, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 355, "output_tokens": 99}
{"timestamp": "2026-11-12T02:53:33+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Found my new absolute go-to sneakers on Poshmark for $48 and I am never taking them off. They give the ultimate 90s streetwear vibe when I wear them with baggy denim and a vintage jacket. Such a good score!", "selected_item_id": "lst_019", "latency_s": 2.79, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 376, "output_tokens": 115}
{"timestamp": "2026-11-12T02:53:37+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement for this 90s floral silk midi. Paired it with chunky sneakers and a zip hoodie for that ultimate grunge-meets-feminine moment, but it’s just as good with a denim jacket and combat boots. Grabbed it for $30 and she’s officially live on my Depop! 🥀✨", "selected_item_id": "lst_013", "latency_s": 3.63, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 397, "output_tokens": 142}
```
