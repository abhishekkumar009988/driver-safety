# 🎥 Veo 3 Prompt Pack — Fog Reveal + Real Look + Multi-Camera Continuity

> Aapki requirements ke hisaab se banaya gaya:
> 1. Face reveal **nahi** — fog / smoke / colour se entry, face hamesha dhaka hua
> 2. Video **AI na lage** — real, natural, "genuine" feel (ladna, hasna, smile — sab real lage)
> 3. **Do stories connected** — ek dusre se juda hua
> 4. **4–6 camera angles** — same moment, alag-alag nazariye se
> 5. Frames **juda hua lagein** — alag-alag singles na lagin, seamless continuation

---

## 🌫️ PART 1 — Fog / Smoke Face Reveal (density ramp)

Poora idea: character **fog/smoke ke andar se** aata hai. Face kabhi poora clear nahi hota.
Density **zyada** rakho — 70–90%. Har stage ka apna shot hai.

### Stage 1 — Full fog (character dikhta hi nahi)
```
9:16 cinematic shot, empty night street, extremely dense rolling fog filling the frame,
thick volumetric smoke with deep teal and amber light shafts cutting through,
no person visible yet, only fog movement and distant streetlight glow,
slow handheld camera drifting forward, shot on 35mm film, heavy film grain, 24fps, 6 seconds

NEGATIVE: person, figure, face, text, watermark, cartoon, video game look
```

### Stage 2 — Silhouette (shape aata hai, face 0%)
```
9:16 cinematic shot, same night street, same dense rolling fog, deep teal and amber haze,
a dark human silhouette slowly emerging from the smoke, completely backlit, only the outline
of shoulders and head visible, face 100% hidden in shadow and fog, smoke swirling around
the figure, low angle, slow push-in, 35mm film, heavy grain, 24fps, 6 seconds

NEGATIVE: visible face, facial features, front light on face, HD clean look, CGI, cartoon
```

### Stage 3 — Partial (peeth / kandha / haath, face still hidden)
```
9:16 cinematic shot, same location, same dense fog and coloured smoke, camera now closer,
over-the-shoulder and back view of the figure, only shoulder, back and hands visible
through swirling smoke, face completely out of frame, fog density 80%, rim light only,
natural handheld movement, 35mm film grain, 24fps, 6 seconds

NEGATIVE: face visible, looking at camera, facial close-up, plastic skin, smooth CGI look
```

### Stage 4 — Almost reveal (fog thoda khulta hai, par face kabhi clear nahi)
```
9:16 cinematic shot, same fog-filled location, smoke slowly thinning to 60% density,
side profile of the figure partially visible through drifting smoke, eyes and mouth
obscured by shadow and haze, light catches only the jawline edge and collar,
camera holds steady with tiny handheld sway, 35mm film, deep teal-amber grade, 6 seconds

NEGATIVE: clear face, frontal face, recognizable identity, sharp facial detail,
beauty retouch, glossy skin, CGI, anime
```

**Fog density control words (prompt mein direct daalo):**
`extremely dense fog` → `fog density 80%` → `fog density 60%` → `thin haze`
Smoke colour options: `deep teal smoke` / `warm amber smoke` / `smoke + dust mixture` / `cold blue haze`

> 💡 **Trick:** Face reveal ke 3 shot ke beech **15–25% overlap** rakho (Part 4 dekho) — reveal slow aur natural lagega, cut nahi lagega.

---

## 🎭 PART 2 — "AI na lage" Realism Rules (sabse important)

Aapki shikayat sahi hai — AI video **fake/plastic** lagta hai kyunki prompt mein "cinematic masterpiece, 8k, hyper-realistic" jaise words hote hain. Ye words **AI look** paida karte hain.

### ❌ Ye words **kabhi** mat use karo (AI look aata hai)
```
masterpiece, 8k, ultra HD, hyper-realistic, perfect face, flawless skin,
beautiful model, glossy, video game, smooth render, cinematic masterpiece
```

### ✅ Ye words use karo (real look aata hai)
```
shot on 35mm film, handheld camera, slight camera shake, 24fps, 180 degree shutter,
natural skin texture with pores, imperfect framing, candid documentary style,
natural available light, unposed, film grain, halation, slight chromatic aberration,
slightly overexposed window, real location, real people, amateur footage feel
```

### Real-feel checklist (har prompt mein 3–4 daalo)
| Cheez | Prompt mein likho |
|-------|-------------------|
| **Skin** | `natural skin texture, pores visible, no retouching, uneven natural lighting on skin` |
| **Camera** | `handheld, slight shake, micro jitters, imperfect framing, sometimes subject partly out of frame` |
| **Light** | `natural available light, practical street lights, inconsistent exposure, blown highlights` |
| **Motion** | `natural human weight, slight stumble, real breathing, blinking, hair movement` |
| **Film** | `35mm film grain, halation around lights, mild chromatic aberration, soft focus edges` |
| **Emotion** | `genuine spontaneous laughter, real smile with eye crinkles, unposed candid emotion` |

### Example: "Do dost lad rahe hai, phir has rahe hai" (real feel)
```
9:16 handheld documentary-style shot, two young men in casual clothes having a friendly
argument on a street, natural gestures, real body language, one pushes the other playfully
then both burst into genuine spontaneous laughter, real smiles with eye crinkles,
available daylight, slight camera shake, imperfect framing, some motion blur,
shot on 35mm film, natural skin texture, 24fps, 6 seconds

NEGATIVE: plastic skin, glossy faces, perfect symmetry, video game, CGI, anime,
over-saturated, music video style, slow motion
```

> 💡 **Emotion ke liye:** "smile" akela nahi likho — `genuine spontaneous laughter`, `unposed`,
> `eyes crinkle from smiling` likho. Isse AI wali fake smile nahi aati.

---

## 🎬 PART 3 — 4–6 Camera Angles (same moment, multi-cam)

Ek hi scene ko 4–6 angles se shoot karo — bilkul film set ki tarah.
**Sab angles mein ye 4 cheezein same rehni chahiye:** location, wardrobe, lighting direction, time of day.

| # | Angle | Lens | Kaam | Face? |
|---|-------|------|------|-------|
| A | **Wide master** | 35mm | Poora scene establish kare | Door — face nahi |
| B | **Over-the-shoulder** | 50mm | Kisi ke kandhe ke peeche se dekhna | Nahi |
| C | **Low angle hero** | 24mm | Power / entry shot | Silhouette |
| D | **Detail insert** | 85mm | Haath, pair, ring, glass, phone | Nahi |
| E | **Back-view follow** | 35mm | Character peeche se chalta hua | Nahi |
| F | **Crowd / reflection** | 50mm | Bheed, mirror, glass reflection | Blurred |

**Multi-cam continuity line (har angle ke prompt mein daalo):**
```
part of a multi-camera sequence, same location, same wardrobe, same lighting direction,
same time of day, same film stock and color grade as the other angles
```

---

## 🔗 PART 4 — Frames ko jodna (alag singles na lagein)

Aapki shikayat: "frames ek dusre se attach nahi lag rahe, alag-alag singles lag rahe hai."
Solution — **3 rules**:

### Rule 1: Overlap (15–25%)
Har naya frame pichhle frame ke **aakhri moment** se shuru ho:
```
continuing from the previous frame, the opening moment overlaps the final moment
of the previous shot, same camera direction, seamless continuation
```

### Rule 2: Motion match
- Frame 1 mein camera **left** pan kar raha tha → Frame 2 bhi **left** se start ho
- Frame 1 mein character **dayein taraf** chal raha tha → Frame 2 mein bhi same direction
- Prompt mein likho: `camera continues its previous movement`, `subject moving in the same direction`

### Rule 3: Grade lock (colour ek jaisa)
Har frame mein **same grade words** repeat karo:
```
same deep teal and amber color grade, same film grain amount, same contrast curve,
same 35mm film stock as previous frames
```

### Match cut trick (do scenes jodne ke liye)
Agar scene change karna hai par connect rakhna hai — **shape/action match** karo:
- Frame A ka end: haath glass uthata hai → Frame B ka start: wahi haath darwaza kholta hai
- Prompt: `match cut on the hand movement, same hand position, same framing size`

---

## 🔗 PART 5 — Do Stories Connect Karna

Do stories ko jodne ke liye ek **"bridge"** chahiye. Ye 4 options mein se koi ek use karo:

| Bridge type | Kaise | Example |
|-------------|-------|---------|
| **Same object** | Ek cheez dono stories mein | Wahi phone / wahi car / wahi ring |
| **Same place** | Dono ek hi jagah ho | Wahi chai tapri, wahi gaon |
| **Same character** | Ek banda dono mein ho | Story A ka hero Story B mein |
| **Same ending→start** | Story A ka end = Story B ka start | A mein fog, B fog se shuru |

**Bridge prompt line:**
```
this shot is the bridge between the two storylines, same fog and color palette
as the previous sequence, same location and lighting, visual echo of the earlier scene
```

---

## 🧩 PART 6 — Veo 3 Master Prompt Format

Veo 3 mein prompt is order mein likho (best results):

```
[SHOT TYPE + ASPECT RATIO]: 9:16 handheld cinematic shot,
[LOCATION + TIME]: night street, dense fog, deep teal and amber lights,
[SUBJECT — face hidden]: a tall figure in a dark kurta, seen from behind, silhouette,
[ACTION]: slowly walks through swirling smoke, shoulders moving naturally,
[CAMERA]: low angle, slow push-in, slight handheld shake,
[LIGHTING]: backlit rim light only, face in complete shadow,
[STYLE]: shot on 35mm film, natural skin texture, film grain, 24fps,
[AMBIENCE/AUDIO]: distant traffic, low wind, footsteps on wet road,
[DURATION]: 8 seconds

NEGATIVE: clear face, facial close-up, plastic skin, CGI look, video game, cartoon,
text, watermark, extra fingers, distorted hands, over-saturated colors
```

> Veo 3 mein **audio prompt** bhi likh sakte ho — ambience se video real lagta hai. Zaroor likho.

---

## ✅ Final Checklist (video se pehle)

- [ ] Research pura? (3+ sources, dates sahi)
- [ ] Story beats 5 lines mein likhe?
- [ ] Face **kahin bhi** clear nahi? (har prompt ka NEGATIVE check karo)
- [ ] Har prompt mein realism words? (`35mm film`, `handheld`, `natural skin texture`)
- [ ] Multi-cam angles mein same wardrobe/light/grade?
- [ ] Har frame mein pichhle frame ka 15–25% overlap?
- [ ] Sample image pehle banaya aur approval liya?
- [ ] AI-look words hata diye? (`8k`, `masterpiece`, `hyper-realistic`)

---

## 📌 Agla step

Jab aap **frames / screenshots is chat mein upload** karoge (main chat box → 📎), main:
1. Aapke frames ko dekhunga — kaunsi story, kaunse characters, kaunsa look
2. Dono stories ka connection point nikalunga
3. Aapke **exact frames ke liye ready Veo 3 prompts** likhunga (fog reveal + realism + multi-cam + overlap lines ke saath)
