# Capstone run log: before

- Produced by: `run_capstone.py` (`one_run`), scoring as worded in `criteria.md`
- Servers: `serve.py` with the cache off; `logs/runs.jsonl` is written by `runlog.py::run_logged`
- When: 2026-11-11 20:20
- Runs: 3, with the whole test repeated each time and nothing changed in between

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A matching query completes | at least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. An impossible query stops before any model call | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Every kind of request leaves one complete log line | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. A warm matching request takes 5.0 s or less | at least 4 of 5 | 5/5 | 3/5 | 4/5 | MISSED |
| 5. One matching run uses 600 tokens or fewer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

A criterion is MET only if every run reaches its target.

## Run 1

- server A rate-limit pauses: 0
- server C rate-limit pauses: 0

### 1. A matching query completes

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:14:31+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the ultimate Y2K baby tee with the cutest pastel butterfly print. Grabbed it on Depop for just $18 and I’m already obsessed. Throwing it on with baggy dark-wash denim and chunky sneakers for that 2000s off-duty model vibe. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.47, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 366, "output_tokens": 112}
{"timestamp": "2026-11-12T02:14:34+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Living out my 90s streetwear dreams in this navy and white striped track jacket. Snagged it on Poshmark for $45 and honestly, I'm never taking it off. Throwing it over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 3.32, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 382, "output_tokens": 125}
{"timestamp": "2026-11-12T02:14:37+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with how good this cropped light wash jacket looks thrown over literally everything. Paid $42 on Poshmark and it’s giving the ultimate effortlessly cool, 90s off-duty model vibe. Snag it before I change my mind and keep it for myself!", "selected_item_id": "lst_007", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 114}
{"timestamp": "2026-11-12T02:14:40+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for just $48 and I am officially in my Y2K model-off-duty era. Going to live in these with baggy denim and a vintage jacket all fall. Honestly, the ultimate lazy-girl street style hack.", "selected_item_id": "lst_019", "latency_s": 2.73, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 375, "output_tokens": 120}
{"timestamp": "2026-11-12T02:14:43+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally found my dream 90s floral slip dress and I am never taking it off. Got this midi beauty on Depop for just $30 and the grunge-meets-feminine styling options are endless. Obsessed with layering it over a white ribbed tank with chunky sneakers, or just throwing an oversized crewneck right over top.", "selected_item_id": "lst_013", "latency_s": 3.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 393, "output_tokens": 135}
```

### 2. An impossible query stops before any model call

- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:14:45+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.31, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:14:46+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.36, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:14:47+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.34, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:14:49+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.38, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:14:50+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.38, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 3. Every kind of request leaves one complete log line

- PASS (expected `ok`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS (expected `ok`): `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS (expected `no_results`): `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS (expected `rejected`): `` -> HTTP 400, 1 new log line(s)
- PASS (expected `model_unavailable`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:15:27+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Obsessed with this little butterfly tee—giving major 2000s pop star off-duty vibes. Got it on Depop for just $18 and I’m already living in it. Paired it with my go-to baggy jeans and a beat-up denim jacket for the ultimate nostalgic look. 🦋✨", "selected_item_id": "lst_002", "latency_s": 5.27, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 118}
{"timestamp": "2026-11-12T02:15:29+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece and I'm obsessed. Snagged this navy and white stripe track jacket for just $45 over on Poshmark. Throw it on with a ribbed tank, baggy denim, and chunky sneakers for that effortless model-off-duty vibe.", "selected_item_id": "lst_004", "latency_s": 2.38, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 388, "output_tokens": 129}
{"timestamp": "2026-11-12T02:15:30+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.42, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:15:30+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:15:37+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 5.36, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 4. A warm matching request takes 5.0 s or less

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:14:31+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the ultimate Y2K baby tee with the cutest pastel butterfly print. Grabbed it on Depop for just $18 and I’m already obsessed. Throwing it on with baggy dark-wash denim and chunky sneakers for that 2000s off-duty model vibe. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.47, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 366, "output_tokens": 112}
{"timestamp": "2026-11-12T02:14:34+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Living out my 90s streetwear dreams in this navy and white striped track jacket. Snagged it on Poshmark for $45 and honestly, I'm never taking it off. Throwing it over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 3.32, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 382, "output_tokens": 125}
{"timestamp": "2026-11-12T02:14:37+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with how good this cropped light wash jacket looks thrown over literally everything. Paid $42 on Poshmark and it’s giving the ultimate effortlessly cool, 90s off-duty model vibe. Snag it before I change my mind and keep it for myself!", "selected_item_id": "lst_007", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 114}
{"timestamp": "2026-11-12T02:14:40+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for just $48 and I am officially in my Y2K model-off-duty era. Going to live in these with baggy denim and a vintage jacket all fall. Honestly, the ultimate lazy-girl street style hack.", "selected_item_id": "lst_019", "latency_s": 2.73, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 375, "output_tokens": 120}
{"timestamp": "2026-11-12T02:14:43+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally found my dream 90s floral slip dress and I am never taking it off. Got this midi beauty on Depop for just $30 and the grunge-meets-feminine styling options are endless. Obsessed with layering it over a white ribbed tank with chunky sneakers, or just throwing an oversized crewneck right over top.", "selected_item_id": "lst_013", "latency_s": 3.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 393, "output_tokens": 135}
```

### 5. One matching run uses 600 tokens or fewer

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:14:31+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the ultimate Y2K baby tee with the cutest pastel butterfly print. Grabbed it on Depop for just $18 and I’m already obsessed. Throwing it on with baggy dark-wash denim and chunky sneakers for that 2000s off-duty model vibe. ✨🦋", "selected_item_id": "lst_002", "latency_s": 3.47, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 366, "output_tokens": 112}
{"timestamp": "2026-11-12T02:14:34+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Living out my 90s streetwear dreams in this navy and white striped track jacket. Snagged it on Poshmark for $45 and honestly, I'm never taking it off. Throwing it over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 3.32, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 382, "output_tokens": 125}
{"timestamp": "2026-11-12T02:14:37+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with how good this cropped light wash jacket looks thrown over literally everything. Paid $42 on Poshmark and it’s giving the ultimate effortlessly cool, 90s off-duty model vibe. Snag it before I change my mind and keep it for myself!", "selected_item_id": "lst_007", "latency_s": 2.57, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 114}
{"timestamp": "2026-11-12T02:14:40+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Scored these chunky white platforms on Poshmark for just $48 and I am officially in my Y2K model-off-duty era. Going to live in these with baggy denim and a vintage jacket all fall. Honestly, the ultimate lazy-girl street style hack.", "selected_item_id": "lst_019", "latency_s": 2.73, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 375, "output_tokens": 120}
{"timestamp": "2026-11-12T02:14:43+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Finally found my dream 90s floral slip dress and I am never taking it off. Got this midi beauty on Depop for just $30 and the grunge-meets-feminine styling options are endless. Obsessed with layering it over a white ribbed tank with chunky sneakers, or just throwing an oversized crewneck right over top.", "selected_item_id": "lst_013", "latency_s": 3.65, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 393, "output_tokens": 135}
```

## Run 2

- server A rate-limit pauses: 0
- server C rate-limit pauses: 0

### 1. A matching query completes

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:16:45+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the absolute cutest butterfly tee on Depop for just $18! Obsessed with this pastel Y2K vibe. Gonna pair it with my go-to baggy jeans and a vintage denim jacket for the ultimate effortless look.", "selected_item_id": "lst_002", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 100}
{"timestamp": "2026-11-12T02:16:48+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece and I’m obsessed. Snagged this navy and white striped track jacket for $45 over on Poshmark. Throwing it on over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.58, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 118}
{"timestamp": "2026-11-12T02:16:55+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It’s giving major off-duty model vibes, whether I throw it over a ribbed tank and khakis or layer it heavy-duty style with a baggy crewneck and combat boots. Such a good closet staple!", "selected_item_id": "lst_007", "latency_s": 6.89, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 372, "output_tokens": 126}
{"timestamp": "2026-11-12T02:17:02+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Obsessed is an understatement. Snagged these chunky platform sneakers on Poshmark for $48 and they instantly complete my whole Y2K streetwear vibe. Can't wait to style them with baggy denim and a vintage jacket all fall.", "selected_item_id": "lst_019", "latency_s": 6.96, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 111}
{"timestamp": "2026-11-12T02:17:05+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement. Found this 90s floral midi on Depop for just $30 and I’m ready to live out all my grunge-romance dreams. Gonna layer it with combat boots and an oversized crewneck for that perfect messy-chic vibe. ✨🖤", "selected_item_id": "lst_013", "latency_s": 3.29, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 117}
```

### 2. An impossible query stops before any model call

- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:17:07+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.4, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:17:08+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.49, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:17:10+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.59, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:17:11+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.61, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:17:13+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.44, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 3. Every kind of request leaves one complete log line

- PASS (expected `ok`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS (expected `ok`): `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS (expected `no_results`): `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS (expected `rejected`): `` -> HTTP 400, 1 new log line(s)
- PASS (expected `model_unavailable`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:17:48+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the ultimate Y2K butterfly baby tee and I’m literally obsessed. Got it for just $18 over on depop and it gives off major 2000s pop star off-duty energy. Styling it with baggy denim and chunky sneakers for the full nostalgic look. ✨🦋", "selected_item_id": "lst_002", "latency_s": 4.92, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 364, "output_tokens": 108}
{"timestamp": "2026-11-12T02:17:51+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found my new go-to sporty 90s streetwear staple. Snagged this navy and white striped track jacket for $45 on Poshmark and I am never taking it off. Throwing it over a ribbed tank and baggy denim for the ultimate off-duty look. 🏃‍♀️💨", "selected_item_id": "lst_004", "latency_s": 2.98, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 384, "output_tokens": 127}
{"timestamp": "2026-11-12T02:17:52+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.19, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:17:52+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:17:59+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 5.72, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 4. A warm matching request takes 5.0 s or less

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- FAIL: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- FAIL: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:16:45+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the absolute cutest butterfly tee on Depop for just $18! Obsessed with this pastel Y2K vibe. Gonna pair it with my go-to baggy jeans and a vintage denim jacket for the ultimate effortless look.", "selected_item_id": "lst_002", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 100}
{"timestamp": "2026-11-12T02:16:48+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece and I’m obsessed. Snagged this navy and white striped track jacket for $45 over on Poshmark. Throwing it on over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.58, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 118}
{"timestamp": "2026-11-12T02:16:55+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It’s giving major off-duty model vibes, whether I throw it over a ribbed tank and khakis or layer it heavy-duty style with a baggy crewneck and combat boots. Such a good closet staple!", "selected_item_id": "lst_007", "latency_s": 6.89, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 372, "output_tokens": 126}
{"timestamp": "2026-11-12T02:17:02+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Obsessed is an understatement. Snagged these chunky platform sneakers on Poshmark for $48 and they instantly complete my whole Y2K streetwear vibe. Can't wait to style them with baggy denim and a vintage jacket all fall.", "selected_item_id": "lst_019", "latency_s": 6.96, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 111}
{"timestamp": "2026-11-12T02:17:05+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement. Found this 90s floral midi on Depop for just $30 and I’m ready to live out all my grunge-romance dreams. Gonna layer it with combat boots and an oversized crewneck for that perfect messy-chic vibe. ✨🖤", "selected_item_id": "lst_013", "latency_s": 3.29, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 117}
```

### 5. One matching run uses 600 tokens or fewer

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:16:45+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found the absolute cutest butterfly tee on Depop for just $18! Obsessed with this pastel Y2K vibe. Gonna pair it with my go-to baggy jeans and a vintage denim jacket for the ultimate effortless look.", "selected_item_id": "lst_002", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 371, "output_tokens": 100}
{"timestamp": "2026-11-12T02:16:48+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s streetwear piece and I’m obsessed. Snagged this navy and white striped track jacket for $45 over on Poshmark. Throwing it on over a white ribbed tank and baggy denim is about to be my entire personality this season.", "selected_item_id": "lst_004", "latency_s": 2.58, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 380, "output_tokens": 118}
{"timestamp": "2026-11-12T02:16:55+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Obsessed with this light wash cropped denim jacket I just scored on Poshmark for $42. It’s giving major off-duty model vibes, whether I throw it over a ribbed tank and khakis or layer it heavy-duty style with a baggy crewneck and combat boots. Such a good closet staple!", "selected_item_id": "lst_007", "latency_s": 6.89, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 372, "output_tokens": 126}
{"timestamp": "2026-11-12T02:17:02+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Obsessed is an understatement. Snagged these chunky platform sneakers on Poshmark for $48 and they instantly complete my whole Y2K streetwear vibe. Can't wait to style them with baggy denim and a vintage jacket all fall.", "selected_item_id": "lst_019", "latency_s": 6.96, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 111}
{"timestamp": "2026-11-12T02:17:05+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Obsessed is an understatement. Found this 90s floral midi on Depop for just $30 and I’m ready to live out all my grunge-romance dreams. Gonna layer it with combat boots and an oversized crewneck for that perfect messy-chic vibe. ✨🖤", "selected_item_id": "lst_013", "latency_s": 3.29, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 385, "output_tokens": 117}
```

## Run 3

- server A rate-limit pauses: 0
- server C rate-limit pauses: 0

### 1. A matching query completes

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:19:07+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found my new holy grail baby tee 🦋 Absolutely living for this butterfly print and had to grab it before someone else did. Snagged it on Depop for just $18 and honestly, nothing beats that Y2K off-duty model energy. Can't wait to style this with some baggy denim and chunky sneakers all spring long!", "selected_item_id": "lst_002", "latency_s": 2.99, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 118}
{"timestamp": "2026-11-12T02:19:10+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Scored this vintage navy track jacket and I'm obsessed with the 90s athletic energy. Grabbed it on Poshmark for $45 and it’s about to live over every white tank and baggy jean combo I own. Seriously the easiest way to look put-together while doing the absolute bare minimum.", "selected_item_id": "lst_004", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 381, "output_tokens": 128}
{"timestamp": "2026-11-12T02:19:13+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Honestly still not over scoring this light wash cropped denim jacket. It’s giving the ultimate off-duty model vibe and I’m so ready to throw it on over a white tank and chunky sneakers. Grabbed it on Poshmark for just $42 and my closet is officially thanking me.", "selected_item_id": "lst_007", "latency_s": 3.12, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 387, "output_tokens": 137}
{"timestamp": "2026-11-12T02:19:17+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Finally scored these chunky white platforms on Poshmark for $48 and I am officially in my Y2K street style era. Can't wait to live in these with baggy denim and a vintage jacket all fall. Literally the best $48 I've spent in a minute.", "selected_item_id": "lst_019", "latency_s": 3.66, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 120}
{"timestamp": "2026-11-12T02:19:36+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Still pinching myself over this 90s floral midi slip dress. It was $30 on Depop and honestly, the grunge-meets-feminine styling potential is endless. I’m picturing it thrown under an oversized crewneck with combat boots, or layered over a ribbed tank for daytime. 🥀🖤", "selected_item_id": "lst_013", "latency_s": 19.46, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 383, "output_tokens": 121}
```

### 2. An impossible query stops before any model call

- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS: `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:19:38+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.26, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:19:39+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.62, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:19:41+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.81, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:19:43+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.69, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:19:44+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.44, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 3. Every kind of request leaves one complete log line

- PASS (expected `ok`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS (expected `ok`): `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS (expected `no_results`): `designer ballgown size XXS under $5` -> HTTP 200, 1 new log line(s)
- PASS (expected `rejected`): `` -> HTTP 400, 1 new log line(s)
- PASS (expected `model_unavailable`): `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:20:22+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "My inner 2000s pop star is losing it over this butterfly baby tee. Found this absolute gem on Depop for just $18 and I am never taking it off. Gonna throw it on with some baggy denim and chunky sneakers for the ultimate off-duty bratz doll energy.", "selected_item_id": "lst_002", "latency_s": 6.68, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 367, "output_tokens": 111}
{"timestamp": "2026-11-12T02:20:24+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Found the ultimate 90s track jacket and my streetwear heart is so happy. Score this navy and white stripe beauty on my Poshmark for just $45. Honestly obsessed with how effortless it looks thrown over a basic tank and baggy denim.", "selected_item_id": "lst_004", "latency_s": 2.73, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 368, "output_tokens": 100}
{"timestamp": "2026-11-12T02:20:26+00:00", "query": "designer ballgown size XXS under $5", "outcome": "no_results", "output": "No listings matched. Try raising the price ceiling, dropping the size filter, or using different keywords.", "selected_item_id": null, "latency_s": 1.3, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:20:26+00:00", "query": "", "outcome": "rejected", "output": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "selected_item_id": null, "latency_s": 0.0, "model_calls": 0, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
{"timestamp": "2026-11-12T02:20:31+00:00", "query": "vintage graphic tee under $30", "outcome": "model_unavailable", "output": "The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.", "selected_item_id": "lst_002", "latency_s": 4.65, "model_calls": 1, "cache_hits": 0, "prompt_tokens": 0, "output_tokens": 0}
```

### 4. A warm matching request takes 5.0 s or less

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- FAIL: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:19:07+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found my new holy grail baby tee 🦋 Absolutely living for this butterfly print and had to grab it before someone else did. Snagged it on Depop for just $18 and honestly, nothing beats that Y2K off-duty model energy. Can't wait to style this with some baggy denim and chunky sneakers all spring long!", "selected_item_id": "lst_002", "latency_s": 2.99, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 118}
{"timestamp": "2026-11-12T02:19:10+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Scored this vintage navy track jacket and I'm obsessed with the 90s athletic energy. Grabbed it on Poshmark for $45 and it’s about to live over every white tank and baggy jean combo I own. Seriously the easiest way to look put-together while doing the absolute bare minimum.", "selected_item_id": "lst_004", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 381, "output_tokens": 128}
{"timestamp": "2026-11-12T02:19:13+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Honestly still not over scoring this light wash cropped denim jacket. It’s giving the ultimate off-duty model vibe and I’m so ready to throw it on over a white tank and chunky sneakers. Grabbed it on Poshmark for just $42 and my closet is officially thanking me.", "selected_item_id": "lst_007", "latency_s": 3.12, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 387, "output_tokens": 137}
{"timestamp": "2026-11-12T02:19:17+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Finally scored these chunky white platforms on Poshmark for $48 and I am officially in my Y2K street style era. Can't wait to live in these with baggy denim and a vintage jacket all fall. Literally the best $48 I've spent in a minute.", "selected_item_id": "lst_019", "latency_s": 3.66, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 120}
{"timestamp": "2026-11-12T02:19:36+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Still pinching myself over this 90s floral midi slip dress. It was $30 on Depop and honestly, the grunge-meets-feminine styling potential is endless. I’m picturing it thrown under an oversized crewneck with combat boots, or layered over a ribbed tank for daytime. 🥀🖤", "selected_item_id": "lst_013", "latency_s": 19.46, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 383, "output_tokens": 121}
```

### 5. One matching run uses 600 tokens or fewer

- PASS: `vintage graphic tee under $30` -> HTTP 200, 1 new log line(s)
- PASS: `90s track jacket in size M` -> HTTP 200, 1 new log line(s)
- PASS: `denim jacket under $50` -> HTTP 200, 1 new log line(s)
- PASS: `platform sneakers size 8` -> HTTP 200, 1 new log line(s)
- PASS: `silk slip dress in midi length under $40` -> HTTP 200, 1 new log line(s)

Log lines written:

```json
{"timestamp": "2026-11-12T02:19:07+00:00", "query": "vintage graphic tee under $30", "outcome": "ok", "output": "Found my new holy grail baby tee 🦋 Absolutely living for this butterfly print and had to grab it before someone else did. Snagged it on Depop for just $18 and honestly, nothing beats that Y2K off-duty model energy. Can't wait to style this with some baggy denim and chunky sneakers all spring long!", "selected_item_id": "lst_002", "latency_s": 2.99, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 365, "output_tokens": 118}
{"timestamp": "2026-11-12T02:19:10+00:00", "query": "90s track jacket in size M", "outcome": "ok", "output": "Scored this vintage navy track jacket and I'm obsessed with the 90s athletic energy. Grabbed it on Poshmark for $45 and it’s about to live over every white tank and baggy jean combo I own. Seriously the easiest way to look put-together while doing the absolute bare minimum.", "selected_item_id": "lst_004", "latency_s": 2.67, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 381, "output_tokens": 128}
{"timestamp": "2026-11-12T02:19:13+00:00", "query": "denim jacket under $50", "outcome": "ok", "output": "Honestly still not over scoring this light wash cropped denim jacket. It’s giving the ultimate off-duty model vibe and I’m so ready to throw it on over a white tank and chunky sneakers. Grabbed it on Poshmark for just $42 and my closet is officially thanking me.", "selected_item_id": "lst_007", "latency_s": 3.12, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 387, "output_tokens": 137}
{"timestamp": "2026-11-12T02:19:17+00:00", "query": "platform sneakers size 8", "outcome": "ok", "output": "Finally scored these chunky white platforms on Poshmark for $48 and I am officially in my Y2K street style era. Can't wait to live in these with baggy denim and a vintage jacket all fall. Literally the best $48 I've spent in a minute.", "selected_item_id": "lst_019", "latency_s": 3.66, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 373, "output_tokens": 120}
{"timestamp": "2026-11-12T02:19:36+00:00", "query": "silk slip dress in midi length under $40", "outcome": "ok", "output": "Still pinching myself over this 90s floral midi slip dress. It was $30 on Depop and honestly, the grunge-meets-feminine styling potential is endless. I’m picturing it thrown under an oversized crewneck with combat boots, or layered over a ribbed tank for daytime. 🥀🖤", "selected_item_id": "lst_013", "latency_s": 19.46, "model_calls": 2, "cache_hits": 0, "prompt_tokens": 383, "output_tokens": 121}
```
