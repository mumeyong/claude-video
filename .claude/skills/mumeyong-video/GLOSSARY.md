# GLOSSARY — tech terms stay English

**Rule:** technical terms are written and spoken **in English, exactly as engineers say them** — never
translated into Indonesian. Indonesian is the glue around them ("aku", "terus", "jadi", "pas"), and Indonesian
affixes on English terms are fine and natural: *di-deploy, di-scale, nge-restart, pod-nya, node-nya*.

Metaphors are allowed (gerbang tol, tagihan bocor) — but when the actual concept is named, use the English term.
A metaphor may introduce a term, never replace it: "gardu baru dibuka — itu **auto-scaling**".

| ✅ Use (English) | ❌ Don't translate to |
|---|---|
| node | mesin, simpul |
| pod, container, cluster | wadah, kontainer (for the k8s object), klaster |
| load balancer | penyeimbang beban, pembagi |
| auto-scaling, scale up / scale down | penskalaan, nambah/nutup sendiri (as the term) |
| request, traffic, peak hour, latency | permintaan, lalu lintas, jam sibuk (in a tech sentence), jeda |
| down, downtime, uptime, crash | tumbang, mati, rusak (for a pod/service) |
| deploy, rollback, restart | menyebarkan, mengembalikan |
| idle | nganggur |
| unattached disk, snapshot, stale | disk yatim, cuplikan, numpuk |
| right-sizing, downsize | ukuran yang pas, kecilin/turunin ukuran (as the term) |
| on-demand / pay-as-you-go | harga eceran |
| reserved instance, subscription, savings plan | langganan tahunan |
| spot instance, interrupt | boleh mati sewaktu-waktu |
| pay-per-use | bayar pas dipakai (as the term) |
| monolith, microservices, serverless | aplikasi lama, layanan kecil |
| users | pengguna (on diagrams) |
| infra, app, API, database | infrastruktur, aplikasi (as labels) |
| auto-shutdown, schedule | dimatiin otomatis, jadwal |
| failed, timeout, error (status labels) | gagal, waktu habis (as status tags) |
| monitoring, observability | pantau, pemantauan (as the term) |

Non-tech everyday words stay Indonesian: tagihan, biaya, hemat, mahal, murah, aman, lemot, rame, sepi, jam kerja.
Loanwords that Indonesians already use naturally are fine either way: migrasi, arsitektur, aplikasi (in casual
narration), server, cloud.

When unsure: **"Would an Indonesian engineer say this word in English at work?"** → yes = keep it English.
