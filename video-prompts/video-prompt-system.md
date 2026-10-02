# 🎬 Video Prompt System — Real Story + Hidden Face + Frame Extension

> Ye file har "real story" video ke liye ready-to-use prompt system hai.
> Prompt text **English** mein likha hai (AI video tools — Veo 3, Sora, Kling, Runway — English best samajhte hain).
> Nirdesh (instructions) Hinglish mein hain.

---

## 📋 Kaam karne ka 4-step flow

| Step | Kya karna hai | Output |
|------|---------------|--------|
| **1. Research** | Real story dhoondo — 3+ sources, dates, kaun kya bola | Story beats (5 lines) |
| **2. Shot list** | Story ko 8–10 frames mein todo | Frame-by-frame plan |
| **3. Sample image** | Pehla/sabse important frame ka **sample image** banao → owner se approval lo ("haan story right hai") | Approved look |
| **4. Video** | Har frame ka prompt → generate → **har frame mein pichhle frame ka 15–25% part repeat karo** (extension continuity) | Final video |

**Rule:** Sample image approve hone se pehle video generation shuru **nahi** karni. Pehle "yes, story right hai" — phir video.

---

## 🚫 Rule 1 — Face kabhi clear nahi dikhna chahiye

Ye privacy ke liye bhi achha hai aur "reveal" wale videos mein mystery build karta hai.

### Face-hiding techniques (koi bhi 2–3 use karo, har shot mein)
- **Back view** / over-the-shoulder shot
- **Silhouette** — strong backlight, chehra andhera
- **Face out of frame** — sirf haath, kandha, peeth, pair dikhe
- **Motion blur** — tez chalte hue, face blur
- **Shadow / hood** — cap, helmet, hood, dupatta, shadow mein aadha chehra
- **Crowd occlusion** — log beech mein aa jayein
- **Focus shift** — camera face par focus hi na kare, haath/object par focus
- **Low light / night shoot** — sirf rim light (kinare se roshni), chehra kaala

### Prompt mein ye likhna zaroori hai
**NEGATIVE (kya nahi chahiye):**
```
clear face, front-facing face, facial close-up, recognizable identity, sharp facial features,
photorealistic face of a real person, celebrity face, direct eye contact with camera
```
**POSITIVE (kya chahiye):**
```
face not visible, back view, over-the-shoulder, silhouette, rim lighting, subject in shadow,
camera focused on hands, mysterious anonymous figure, no facial detail
```

> ⚠️ Real person ke baare mein ho toh: sirf verified facts bolo, "alleged / kaha jaata hai" jaise words use karo, aur koi bhi jhooti ilzaam mat lagao. Face hide karna achhi practice hai — isi tarah rakhna.

---

## 🔍 Rule 2 — Real story pehle research karo (video se pehle)

**Research checklist:**
1. **Kya hua?** — 3 alag sources (news article, video, official statement)
2. **Kab hua?** — date + time (video mein "aaj se X saal pehle" type framing)
3. **Kahan hua?** — exact jagah, mausam, time of day (visuals ke liye)
4. **Kaun involved?** — naam/role. Real person ka naam lena hai? Face hide + fair language
5. **Story ka turn** — wo ek moment jispe video ka hook bana hai
6. **Ending/payoff** — story ka lesson ya result

**Story beats (5 lines mein likho — video ka skeleton):**
```
HOOK (0–3s):   ______________________
CONTEXT:       ______________________
TURNING POINT: ______________________
VIP ENTRY:     ______________________
PAYOFF/END:    ______________________
```

---

## 🚗 Rule 3 — "VIP Entry" shot recipe

VIP entry ek signature moment hai — ise aise banao:

**Shot list (entry sequence — 4 shots):**
1. **Establish** — location wide shot, crowd/gate/road dikhe. *Prompt:* `wide establishing shot, crowd waiting, empty road, tension in the air, cinematic, 9:16`
2. **Build-up** — chehre (VIP ke nahi — logon ke reactions), murmur, sirens. *Prompt:* `crowd turning their heads, people whispering, security guards adjusting position, shallow depth of field, face not visible`
3. **THE ENTRY** — VIP ka silhouette/back view, low angle, slow motion, dust/light. *Prompt:* `low angle shot, powerful figure walking through gate, seen from behind, silhouette against light, slow motion, dust particles in air, no face visible, epic entrance, cinematic anamorphic lens`
4. **Aftermath** — peeth peeche jaate hue, doors band, ya car nikal jaati hai. *Prompt:* `figure walking away from camera, back view, crowd watching, camera slowly pushes in, cinematic`

**VIP entry ka golden rule:**
> Camera **VIP ke peeche** rahega, **VIP ke saamne nahi**. Face automatically hidden.

---

## 🔗 Rule 4 — Frame extension (frame 1 ka part frame 2 mein)

Aap chahte ho ki agla frame pichhle frame ka **extended version** lage — matlab dono shots juda hua ek continuous scene lagein. Iske liye:

### Continuity rules (har frame pair par apply karo)
| Cheez | Rule |
|-------|------|
| **Camera** | Frame 1 jis direction mein move ho raha hai, Frame 2 usi direction se shuru ho |
| **Overlap** | Frame 2 ka pehla 15–25% bilkul Frame 1 ke **aakhri moment** jaisa dikhe |
| **Wardrobe** | Same kapde — exact color/layer likho prompt mein |
| **Lighting** | Same time of day, same roshni ki direction (left se / right se) |
| **Location** | Same jagah, same background objects |
| **Lens** | Same focal length feel (35mm wide / 85mm tight) |

### Frame 2 ke prompt mein ye line daalo
```
continuing from the previous frame, same location, same wardrobe, same lighting direction,
camera continues its movement from where it stopped, opening moment overlaps the last moment
of the previous shot, seamless continuation, same film grain and color grade
```

### Example: Frame 1 → Frame 2 (extension)

**FRAME 1 PROMPT:**
```
9:16 cinematic shot, night street outside a gate, crowd waiting, a powerful figure in a
dark kurta walks through the gate seen from behind, back view only, silhouette against
warm gate lights, slow motion, dust in air, camera slow push-in, no face visible,
35mm anamorphic, moody teal and amber grade, 6 seconds
NEGATIVE: clear face, front view, facial detail
```

**FRAME 2 PROMPT (extension):**
```
9:16 cinematic shot, continuing from the previous frame, same night street, same dark kurta,
same warm gate lights from the left, camera continues pushing in as the figure walks away
from camera, back view only, crowd parts around him, dust still in air, no face visible,
35mm anamorphic, moody teal and amber grade, same film grain, 6 seconds
NEGATIVE: clear face, front view, facial detail, different location, different lighting
```

Frame 2 ka pehla part Frame 1 ke end se **match** karta hai → lagta hai ek hi shot ka extension hai. ✅

---

## 🧩 Master Prompt Template (copy-paste karo)

```
[ASPECT RATIO] cinematic shot, [LOCATION + TIME OF DAY],
[SUBJECT — face never visible: back view / silhouette / over-the-shoulder],
[ACTION — what is happening],
[CAMERA — angle + movement: slow push-in / pan left / low angle / handheld],
[LIGHTING — direction + mood],
[STYLE — 35mm / anamorphic / film grain / color grade],
[AUDIO — ambient sound / music mood],
[DURATION — 5–8 seconds]

NEGATIVE: clear face, front-facing face, facial close-up, recognizable identity,
sharp facial features, direct eye contact with camera, text, watermark, extra fingers
```

---

## 🖼️ Sample image approval step

Video banane se pehle:
1. Sabse important frame (usually **VIP entry** ya **hook frame**) ka image generate karo
2. Owner/user ko dikhao: *"Ye look sahi hai? Story right hai?"*
3. **"Haan"** mile → tabhi video generation shuru
4. "Nahi" mile → prompt fix karo, sample dobara banao

---

## 📁 Agla kadam

Ye file ek **system/template** hai. Jab aap is chat mein apni **images aur story** upload karoge,
main isi format mein aapke specific video ke **ready prompts** bana dunga:

- `video-prompts/<story-name>/01-story-beats.md` — research + beats
- `video-prompts/<story-name>/02-shot-list.md` — frame-by-frame plan
- `video-prompts/<story-name>/03-prompts.md` — sabhi frames ke ready prompts (extension lines ke saath)
