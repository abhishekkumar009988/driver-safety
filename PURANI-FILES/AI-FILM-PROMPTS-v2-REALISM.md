# 🎬 AI-FILM-PROMPTS **v2 — REALISM PACK**
### Veo 3.1 ke liye · Do stories · 29 shots · 6 cameras · "AI jaisa nahi lagta" fix

> **Kaise use karo:** Ye file **director's kit** hai. Section 1 aur 2 (Character Lock + Style Lock) ek baar bharo — phir **har shot prompt me wahi lines verbatim copy-paste** karo. Yahi ek cheez character ko "same banda" rakhne me sabse zyada kaam karti hai (research: identity block simplify karne pe consistency ~40% gir jaati hai).
>
> **⟨Angle brackets⟩** wali jagah apni detail daalo. Baaki sab as-is use kar sakte ho.

---

## 📌 0. QUICK START — 5 step

| Step | Kaam | Kyu |
|---|---|---|
| 1 | Section 1 me **Character Lock** bharo (A, B, Heroine A, Heroine B) | Chehra har shot me same rahega |
| 2 | Section 2 ka **Style Lock** block bharo (lens, grade, light, 24fps) | Har clip ka look match karega |
| 3 | Section 4 se **shot uthao** → uske prompt me `LOCK-A` + `LOCK-STYLE` paste karo | Chhota prompt, bada control |
| 4 | Section 5 ke **negative block** ko har prompt ke end me lagao | Wax/plastic/AI look band |
| 5 | Generate → Section 10 ka **QC checklist** → phir Section 9 ka **post pass** | Yahi "real" ka last 20% hai |

**Tool:** Veo 3.1 (Flow / Gemini / API)
**Model variants:** `veo-3.1-generate-preview` (quality) · `veo-3.1-fast` (test rips ke liye — pehle Fast pe 2-3 take, final Standard pe)
**Clip length:** 4s / 6s / 8s · **AR:** 9:16 (Reels) ya 16:9 · **fps:** 24 (cinema cadence — 30 nahi)
**Ek clip = ek action.** Do action ek clip me = drift. Tod ke banao, edit me jodo.

---

## 🔒 1. CHARACTER LOCK — yahan apna cast likho

> Rule: **har prompt me poora block, jaisa hai waisa** (word-for-word). Short karne ka mann kare to yaad rakhna — chhota karne pe chehra badal jaata hai.

### `LOCK-A` — HERO A ⟨Story 1 ka ladka⟩
```text
A ⟨22–25⟩-year-old ⟨Indian⟩ man, ⟨5'10"⟩ tall, lean athletic build with broad shoulders,
oval face with a defined jawline and light stubble, medium-brown skin with visible pores and
natural texture, thick dark eyebrows, deep-set dark brown eyes, straight nose, ⟨short wavy black hair,
side-parted⟩, one small mole ⟨below the left eye⟩, ⟨navy blue oxford shirt with sleeves rolled to
elbow, dark grey chinos, brown leather strap watch, silver ring on right hand⟩.
```
### `LOCK-B` — HEROINE A ⟨Story 1 ki ladki⟩
```text
A ⟨21–24⟩-year-old ⟨Indian⟩ woman, ⟨5'5"⟩ tall, slim, oval face with high cheekbones and a soft
rounded chin, warm wheatish skin with visible pores and fine facial hair, long dark brown hair
⟨loose with a few strands falling over the forehead⟩, almond-shaped dark eyes with natural lashes,
⟨small silver stud earrings, mustard yellow kurta with a thin printed dupatta, oxidized silver bangles⟩.
```

### `LOCK-C` — HERO B ⟨Story 2 ka ladka⟩
```text
A ⟨24–27⟩-year-old ⟨Indian⟩ man, ⟨5'11"⟩ tall, broad-shouldered and slightly stocky, square face
with a strong jaw and thick black beard trimmed short, deep-brown skin with visible texture, thick
eyebrows, warm dark eyes, ⟨shaved-sides black hair with a top knot⟩, small scar on the right eyebrow,
⟨khaki Pathani kurta, dark grey shawl over one shoulder, black leather sandals⟩.
```
### `LOCK-D` — HEROINE B ⟨Story 2 ki ladki⟩
```text
A ⟨20–23⟩-year-old ⟨Indian⟩ woman, ⟨5'4"⟩ tall, slim with soft shoulders, round face with dimples
on both cheeks, fair-wheatish skin with visible pores, very long dark hair ⟨single braid over the
left shoulder⟩, kohl-lined dark eyes, ⟨deep red phulkari dupatta draped over the head and falling
over the right shoulder, green salwar suit, small gold jhumkas, a thin gold nose ring⟩.
```

### 🔧 Character Consistency — 5 rules jo actually kaam karte hain
1. **Verbatim rule** — identity block har prompt me bilkul same.
2. **Ingredients to Video** — pehle 2-3 clean reference images banao (Nano Banana Pro / Gemini image), phir **up to 3 ingredients**: `[character] + [location] + [style]`. **Character ingredient sabse pehle** rakho (order = priority).
3. **Seed lock** — pehla sahi take ka seed note karo, usi seed pe variations banao.
4. **Light jump mat karo** — ek clip din ka, dusra raat ka = face drift. Scene change karna ho to **transition ke waqt** bolo: *"time jump to dusk; maintain the same character and wardrobe."*
5. **Canonical portrait** — ek clean front-facing portrait sabse pehle lock karo. Wahi close-ups ka anchor hai.

---

## 🎨 2. STYLE LOCK — ek block, sab shots me same

```text
LOCK-STYLE:
Photorealistic cinematic footage, shot on a ⟨35mm/50mm⟩ lens at T1.8, shallow depth of field,
24 fps with a 180-degree shutter and natural motion blur, subtle 35mm film grain,
true-to-life skin tones with visible pores and subsurface light scattering,
motivated ⟨golden-hour / window / tube-light⟩ source lighting with soft directional shadows,
⟨warm amber and teal shadows⟩ colour grade, documentary realism, no HDR bloom, no oversaturation.
```

**Lens cheatsheet — kis shot me kaunsa:**
| Lens | Kab | Feel |
|---|---|---|
| 24mm | Establishing, wide, drone | Jagah dikhata hai, thoda distortion |
| 35mm | Master + handheld walk | Natural, documentary |
| 50mm | Medium, dialogue, OTS | "Aankh jaisa" |
| 85mm | Close-up, emotion, smile | Face ko flat karta hai, background melt |

---

## 🎥 3. 6-CAMERA PACK — 4-6 camera ek scene me kaise

| ID | Setup | Kab use karo | Prompt phrase |
|---|---|---|---|
| **CAM-1** | Wide master, locked-off ya slow dolly | Scene kholne ke liye, ek baar | `locked-off wide establishing shot, static camera` |
| **CAM-2** | Medium handheld, gentle drift | Main action, sabse zyada | `medium handheld shot with subtle organic camera drift` |
| **CAM-3** | Over-the-shoulder | Jab do log aamne-saamne hain | `over-the-shoulder shot from behind ⟨character⟩, shallow focus on ⟨the other⟩` |
| **CAM-4** | Close-up 85mm, slow push-in | Emotion, smile, aankh, kiss se pehle | `close-up at 85mm, slow push-in, focus on the eyes` |
| **CAM-5** | Insert / low-angle detail | Haath, dupatta, paer, anguthi, prop | `low-angle insert shot, macro detail on ⟨hands/fabric⟩` |
| **CAM-6** | Top / drone / POV | Scene break, transition, scale | `slow overhead drone shot rising vertically` |

### ✂️ Cut rhythm rules (yahi "AI lagta hai" ko maarta hai)
- **Kabhi same shot-size back-to-back mat lagao.** Wide → Close → Medium → Insert = rhythm.
- **Cut on action** — jab haath uth raha ho, dupatta ud raha ho, kadam pad raha ho.
- **180° rule** — dono characters ke beech ek line imagine karo, camera us line ko cross na kare.
- **Har 3-4 shot me ek naya size** zaroor.
- **Slow push-in** > zoom. Zoom AI me sabse zyada fake dikhta hai.
- **Foreground occlusion** add karo — darwaze se, patton ke beech se, kandhe ke upar se shoot. Ye ek cheez instantly "shot on set" feel deti hai.

---

## 🎞️ 4. THE 29-SHOT STRUCTURE — do stories, ek reel

**Structure:** `STORY A (1-12)` → `STORY B (13-22)` → `MERGE (23-29)`
**Do merge models (Section 7 me detail):** Model-1 Parallel (dono couples same beat pe) · Model-2 Flashback (B = past)
**Total:** 29 shots × ~2.5s ≈ **72 sec**
**Prompt method:** Chhote clips alag-alag banao (ek clip = ek shot). Ya 8s clip me **timestamp prompting**:

```text
[00:00-00:03] ⟨shot 1 description⟩
[00:03-00:06] ⟨shot 2 description⟩
[00:06-00:08] ⟨shot 3 description⟩
```
> 2 second se chhota beat = flicker lagta hai. Isliye 3s beats best.

---

### 🅰️ ACT 1 — STORY A (Shots 1–12) · *"pehli nazar → pehla haath"*

| # | ~t | CAM | Shot | Paste-ready core prompt (aage `LOCK-A`+`LOCK-STYLE`+`NEG` lagao) |
|---|---|---|---|---|
| 1 | 0:00 | CAM-1 | Establishing | `Locked-off wide establishing shot of ⟨college courtyard at golden hour⟩, dust motes floating in the low sun, ⟨LOCK-A⟩ walks in from frame right at an unhurried pace, camera static` |
| 2 | 0:03 | CAM-5 | Insert feet | `Low-angle insert, macro detail of his leather sandals kicking up fine dust on ⟨gravel path⟩, single measured step, camera static` |
| 3 | 0:05 | CAM-3 | OTS see her | `Over-the-shoulder shot from behind ⟨LOCK-A⟩, shallow focus racking from his shoulder to ⟨LOCK-B⟩ standing with ⟨books in her arms⟩` |
| 4 | 0:08 | CAM-4 | Her smile | `Close-up at 85mm, slow push-in on her face as a small unguarded smile forms — lips part first, then the cheeks lift, then the eyes crease` |
| 5 | 0:11 | CAM-2 | His reaction | `Medium handheld, subtle drift; his shoulders drop a centimetre as he exhales, weight shifting onto the right foot, jaw relaxing` |
| 6 | 0:13 | CAM-5 | Hands | `Insert close-up on both hands as he takes the ⟨books⟩ from her — his fingers brush the back of her hand for a half-second, then withdraw` |
| 7 | 0:16 | CAM-4 | Eye contact | `Close-up on her eyes flicking up to meet his, then quickly dropping to the ground; a strand of hair falls across the cheek` |
| 8 | 0:18 | CAM-2 | Walk together | `Medium handheld tracking shot moving with them from the side, both walking in step on the ⟨path⟩, shoulders almost touching, mid-frame` |
| 9 | 0:21 | CAM-6 | Top/scale | `Slow overhead shot rising vertically above them as they walk between the ⟨trees⟩, long shadows stretching` |
| 10 | 0:24 | CAM-4 | Laugh beat | `Close-up; she laughs with her whole body — head tipping back, nose crinkling, one hand covering her mouth too late` |
| 11 | 0:26 | CAM-5 | Dupatta/odhna | `Insert shot, macro on ⟨her dupatta⟩ as a breeze lifts a corner, fabric rippling from the pinned end outward with real weight, then settling` |
| 12 | 0:29 | CAM-2 | Near hold | `Medium two-shot handheld; he reaches and tucks the loose strand of her hair behind her ear — the movement is slow, hesitant, thumb lingering one extra beat` |

---

### 🅱️ ACT 2 — STORY B (Shots 13–22) · *"second jodi, alag duniya"*

| # | ~t | CAM | Shot | Paste-ready core prompt |
|---|---|---|---|---|
| 13 | 0:32 | CAM-1 | Establishing | `Locked-off wide establishing shot of ⟨a rain-wet village lane at dusk⟩, steam rising from ⟨chai stall⟩, ⟨LOCK-C⟩ stands with one foot on a step, camera static` |
| 14 | 0:34 | CAM-4 | Her intro | `Close-up at 85mm, slow push-in; ⟨LOCK-D⟩ glances over her shoulder, ─ the dupatta slipping forward off her hair in one clean motion` |
| 15 | 0:37 | CAM-5 | Dupatta odhna | `Insert, macro on ⟨deep red phulkari dupatta⟩ being drawn over her head; the fabric catches the light, falls with visible weight, the embroidered edge settling along the jawline` |
| 16 | 0:39 | CAM-3 | OTS | `Over-the-shoulder shot from behind ⟨LOCK-D⟩, focus on ⟨LOCK-C⟩ across the lane, rain beads on his shawl, he looks up` |
| 17 | 0:42 | CAM-2 | Walk | `Medium handheld, camera drifting with him as he crosses the lane through shallow puddles, water splashing at ankle height, reflections breaking` |
| 18 | 0:45 | CAM-5 | Hands | `Insert, macro: two sets of hands reaching for the same ⟨steel chai glass⟩, fingers meeting on the metal, steam curling between them` |
| 19 | 0:47 | CAM-4 | Held look | `Close-up on his face; he says nothing, jaw tight, a small nod — breath visible in the cold air` |
| 20 | 0:50 | CAM-3 | Hold | `Over-the-shoulder reversed; she wraps ⟨the dupatta⟩ tighter around her shoulders and steps half a pace closer, chin lifting` |
| 21 | 0:52 | CAM-2 | Warmth | `Medium handheld two-shot, the ⟨stall lantern⟩ swinging gently between them, warm light flickering across both faces, rain audible` |
| 22 | 0:55 | CAM-6 | Transition | `Slow overhead shot pulling up away from the lane, the two figures shrinking between wet rooftops` |

---

### 🔗 ACT 3 — MERGE (Shots 23–29) · *"dono kahaniyan ek jagah"*

| # | ~t | CAM | Shot | Paste-ready core prompt |
|---|---|---|---|---|
| 23 | 0:58 | CAM-5 | **Prop bridge** | `Insert, macro on ⟨the same silver ring / same dupatta pattern / same photograph⟩ — the exact prop that appears in both stories, single slow tilt across it` |
| 24 | 1:01 | CAM-2 | **Match cut** | `Medium shot of ⟨LOCK-A⟩ turning his head to the left at the same speed and angle as ⟨LOCK-C⟩ — matched framing, matched timing` |
| 25 | 1:03 | CAM-4 | **Match cut** | `Close-up of ⟨LOCK-B⟩'s smile cut against ⟨LOCK-D⟩'s smile — identical framing, identical duration, one continuous breath` |
| 26 | 1:06 | CAM-2 | **Hug** | `Medium handheld two-shot; they step into a full hug — her forehead into his shoulder, his arm coming over her back, his hand settling flat between her shoulder blades, both exhaling, fabric compressing under the grip` |
| 27 | 1:09 | CAM-4 | **Hold** | `Close-up at 85mm, his palm cupping the side of her face, thumb tracing once along the cheekbone, her eyes closed then opening` |
| 28 | 1:12 | CAM-5 | **Detail** | `Insert, macro: her fingers closing around a fold of his shirt at the back, knuckles going pale, then releasing slightly` |
| 29 | 1:14 | CAM-6 | **End** | `Slow crane shot rising above ⟨both couples⟩ as the last light leaves ⟨the location⟩, the frame filling with ⟨haze / dust / rain⟩, camera still climbing as it fades` |

---

## 🤝 5. HOLD · ODHNA · HUG · KISS — physics wala tarika

> **Asli raaz:** AI ko "emotion" nahi, **weight aur contact** samjhao. "They hug romantically" = plastic. "His hand flattens between her shoulder blades, fabric compresses" = real.

### 🫂 HOLD / HUG
```text
a full weighted embrace — her forehead pressing into the curve of his shoulder,
his right arm coming fully over her back, his hand settling flat between her
shoulder blades, fingers spread; the fabric of his shirt compressing and folding
under the grip; both exhaling at once, shoulders lowering; a half-beat of
stillness before either moves
```
**Kabhi mat likho:** "he holds her tightly, feeling emotional" → ye AI ko floaty banata hai.

### 🧣 ODHNA / DRAPE (dupatta, shawl, chunni)
```text
the ⟨deep red phulkari dupatta⟩ lifted and drawn over her head in one continuous
motion — the fabric catching the light as it rises, then falling with visible
weight along the crown of the head and down the right shoulder; the embroidered
edge settling against her jawline; the loose end swinging once and coming to rest
```
**Physics keywords jo asli banate hain:** `visible weight` · `fabric rippling from the pinned end outward` · `settling` · `half-second of over-swing` · `folds compressing` · `tension at the shoulder`
**Mat likho:** "dupatta flying beautifully" → ye saree-catalog slow-mo CG look dega.

### 💋 KISS — honest baat
Veo 3.1 lambe lip-lock pe **morph, jaw melt, teeth artifacts** banata hai. Teen tested jugaad:

| Tarika | Prompt | Kyu chalta hai |
|---|---|---|
| **A. Almost-kiss + cut** | `he leans in until their foreheads touch, both eyes closing, breath shared — cut before contact` | Tension zyada, artifact zero. Edit me cut maaro. |
| **B. Reveal after cut** | Shot 1: lean in. Shot 2 (new clip): `they separate, both smiling, her hand still on his chest` | Audience khud bhar deti hai. Cinematic. |
| **C. Side-profile silhouette** | `extreme close-up in profile silhouette, backlit, their faces merging into one dark shape` | Silhouette me detail nahi dikhti = artifact chhup jaate hain |

### 😊 SMILE / LAUGH — micro-expressions ka order
```text
a genuine unforced laugh — the lips part first, then the cheeks lift and push into
the lower eyelids, then the eyes crease at the outer corners, head tipping back a
few degrees, one hand rising to cover the mouth half a beat too late
```
**Order yaad rakho:** `lips → cheeks → eyes → head → hand`. Yahi human order hai. Ulta likhne pe AI "fake smile" banata hai.

---

## ⚠️ 6. "AI LAGTA HAI" — 14 GALTIYA + EXACT FIX

> Apne purane video pe ye table chalao. Jo bhi tick ho, uski fix lapak lo.

| # | Galti (jo dikhti hai) | Kyu hota hai | ✅ Prompt fix | 🧪 Post fix |
|---|---|---|---|---|
| 1 | **Plastic/waxy skin** | Model ne pores average kar diye, subsurface scattering missing | `visible skin pores, natural skin variation, fine facial hair, subsurface light scattering, natural oil sheen` | Skin-smoothing OFF. Denoise 15–30 (0–100 me) |
| 2 | **Floaty motion, weight nahi** | Physics sim nahi, statistical guess | `heel-to-toe strike, weight shifting onto the right foot, fabric compressing under the grip, dust kicking up` | Slow-mo 0.5–0.75x |
| 3 | **Har shot same size** | Boring coverage = "staged" feel | Shot sizes ka **rhythm**: W→CU→M→Insert | Edit me re-cut |
| 4 | **Camera zoom/spin kar raha** | Conflicting camera instructions | **Ek hi** move likho: `slow push-in` YA `gentle pan`. Kabhi dono nahi | Transition se chhupao |
| 5 | **Chehra cut pe badal gaya** | Identity block chhota/rephrase ho gaya | `LOCK` block **verbatim**, + character **ingredient image**, + same seed | Mask-based micro-fix |
| 6 | **Background morph/slide** | High-frequency detail temporal lock ke bina | Locked-off ya **simple** move; background ko simple rakho (`plain wall, simple alley`) | Background replace karo |
| 7 | **Motion blur missing / judder** | Cadence galat | `24 fps, 180-degree shutter, natural motion blur` | 24fps pe conform karo |
| 8 | **HDR bloom / oversaturation** | Model ka glossy default | `natural skin tones, no HDR bloom, no oversaturation, limited highlight bloom` | Grade film look ki taraf |
| 9 | **Set "khaali" lag raha** | Atmosphere missing | `dust motes in a shaft of light, steam curling, haze, wind-blown leaves, water on the ground` | Grain + haze pass |
| 10 | **Ek clip me 3 action** | Model confuse = drift | **Ek clip = ek action.** Tod ke banao | Edit me jodo |
| 11 | **Haath/ungli kharab** | Hands high-variance data | `natural hand pose, five-finger anatomy, relaxed fingers` — aur haath ko **simple contact** me rakho, fast gesture avoid | Shot trim / insert se replace |
| 12 | **Sab perfectly lit** | Motivated source nahi | `single motivated ⟨window/lantern/tube light⟩, soft directional shadows, deep falloff` | Contrast badhao |
| 13 | **Sab kuch focus me** | Aperture feel missing | `shallow depth of field, T1.8, background falling into soft bokeh` | Blur vignette |
| 14 | **Sound flat/na hone ke barabar** | Audio ko baad me soch te ho | Har prompt me alag line: `Audio: rain on tin, distant traffic, fabric rustle, no music` | Foley + room tone add karo |

---

## 🚫 7. NEGATIVE PROMPT LIBRARY (copy-paste)

> Rule: **negative me "no / don't" mat likho** — sirf unwanted cheezon ki **list** do. Chhoti rakho (3–7 lines), warna output bland ho jaata hai.

### `NEG-SKIN` (close-ups ke liye — sabse zaroori)
```text
Negative: wax figure skin, plastic sheen, airbrushed face, over-smoothed texture,
beauty-filter look, HDR bloom, oversaturation, over-sharpening
```

### `NEG-MOTION`
```text
Negative: motion blur artifacts, judder, stutter, soap-opera effect, sudden zoom,
camera spin, dutch angle, whip pan, floating objects, weightless movement
```

### `NEG-IDENTITY`
```text
Negative: face morphing, identity drift, changing facial features, age shift,
wardrobe change mid-shot, duplicate limbs, extra fingers, fused digits
```

### `NEG-STYLE`
```text
Negative: cartoon, anime, 3D render, video game look, CGI, illustration,
watermark, text overlay, subtitle, logo
```

### `NEG-ALL` (default — har shot ke end me lagao)
```text
Negative: wax figure skin, plastic sheen, over-smoothed texture, face morphing,
identity drift, extra fingers, fused digits, floating objects, weightless movement,
sudden zoom, camera spin, judder, HDR bloom, oversaturation, over-sharpening,
cartoon, CGI, watermark, text overlay
```

---

## 🔗 8. DO STORIES KO MERGE KARNA — 4 pakke tarike

> **Sach:** Stories AI se merge nahi hoti — **edit me** merge hoti hain. Ye 4 bridges sabse strong hain:

| Bridge | Kaise | Prompt/Edit |
|---|---|---|
| **1. Prop bridge** | Ek cheez dono stories me ho (ring / dupatta pattern / chitthi / photo) | Shot 23: `macro on the ⟨ring⟩ — single slow tilt across it` — same prop dono timelines me |
| **2. Match cut** | Do shots **bilkul same** framing + speed pe | Shot 24/25: `turning his head left at the same speed and angle` — cut pe aankh ko dhyan nahi jaata |
| **3. Sound bridge** | A ki awaaz B ke scene me chalu | Edit: A ki laugh rehne do, B ka shot chalu karo — 1 second |
| **4. Colour bridge** | Grade ek se dusre me shift | Edit: A warm amber → B cool teal, 8 frames ka transition |

**Merge rules:**
- **Ek waqt me ek hi cheez badlo** — na location, na wardrobe, na lens, na light. Colour ya jagah — dono nahi.
- Merge se **2 shot pehle** se bridge ki tayyari shuru karo (prop dikha do, ya colour thoda shift kar do).
- **Parallel montage** me dono couples ka beat **exact match** hona chahiye — warna cheap lagta hai. Metronome pe edit karo (song ke 8-beat pe).
- Flashback model me **visual language alag rakho**: Story B ko thoda soft/diffused, Story A ko sharp/contrast — audience turant timeline pakad leti hai.

---

## 🧪 9. POST-PRODUCTION — "real" ka last 20%

> **Order galat kiya to AI sharpness bake ho jaata hai.**

| Step | Kaam | Setting |
|---|---|---|
| 1 | **Upscale** | Context-aware upscale (Topaz/native Veo 4K upscale) — **pehle** ye |
| 2 | **Slight blur** | Bilkul halka — over-rendered micro-edges tod ne ke liye. Defocus nahi. |
| 3 | **Film grain** | 35mm grain overlay, **~15%** opacity, sab clips pe **same** grain |
| 4 | **Colour grade** | Ek unified film-style grade — sab clips pe same LUT |
| 5 | **Halation** | Highlights pe subtle — "shot on film" signal |
| 6 | **Sound design** | Room tone + foley + ambience. **Silent clip sabse fake lagta hai.** |
| 7 | **Cadence** | Sab clips 24fps pe conform |

---

## ✅ 10. QC CHECKLIST — publish se pehle

- [ ] Chehra, costume, baal — **poore clip me** drift nahi hua
- [ ] Objects size/position hold kar rahe hain (kuch gayab nahi hua)
- [ ] Weight, contact, gravity — sahi lag raha hai
- [ ] Skin/hair/fabric **boil ya swim** nahi kar raha
- [ ] **Paanch ungli** har frame me
- [ ] Motion smooth, blur sahi, koi stutter nahi
- [ ] Kinaare aur background stable
- [ ] Do consecutive shots me **same shot-size** nahi
- [ ] Audio aur image ka scale match karta hai
- [ ] Sab clips ka **grain + grade same**
- [ ] 9:16 me safe area me chehra (top 12% / bottom 15% khaali)

---

## 🎯 11. REUSABLE PROMPT TEMPLATE

```text
[LOCK-STYLE block]

[Shot] ⟨CAM type + subject + action⟩.

Actor detail: ⟨LOCK-X block, verbatim⟩

Action detail: ⟨one action, physical, with weight and contact⟩

Context: ⟨location + time + weather + set dressing⟩

Audio: ⟨ambient + SFX; music only if needed⟩

Duration: ⟨4/6/8⟩s. AR: 9:16. fps: 24.

[NEG-ALL block]
```

---

## 📖 12. FRAME-READ TABLE — *ye hissa tumhare frames aate hi bhara jayega*

> Jab tumhare **29 frames + do videos ke SS** aa jayenge, ye table bhar di jayegi — **guess se nahi, dekh ke**.

| # | Frame | Shot size | Camera | Action | Hold/Contact | Kya AI lagta hai | Fix |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

---

### 📚 Source base
- Google Cloud — *Ultimate prompting guide for Veo 3.1* (timestamp prompting, ingredients-to-video, first/last frame)
- Veo 3.1 API docs — `reference_images` (up to 3), `veo-3.1-generate-preview`
- Community realism research 2026 — temporal consistency, wax-figure effect, post-finishing order (upscale → blur → grain → grade)
- Continuity practice — verbatim identity block, seed discipline, lazy-cut avoidance

---
*AI-FILM-PROMPTS v2 — Realism Pack · banaya gaya tere `driver-safety` workspace me.*
