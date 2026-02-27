# Task Orchestration Rules

Bu kurallar HER TASK icin gecerlidir. Agent, kullanici istegi geldiginde asagidaki adimlarla calisir.

---

## ADIM 0: Hiz Kurallari (Her Zaman Gecerli)

1. **Paralel cagri**: Birbirinden bagimsiz tool call'lari TEK mesajda paralel gonder. Asla sirayla yapma.
2. **Minimum tool call**: Bilgiyi zaten biliyorsan tekrar sorgulama.
3. **Explore agent**: Codebase arama/kesfetme islerinde `explore` subagent kullan, ana context'i kirletme.
4. **Batch okuma**: Birden fazla dosya okumasi gerekiyorsa hepsini tek mesajda paralel oku.
5. **Erken cikis**: Gereksiz dosya okuma veya arama yapma. Soruya cevap verecek minimum bilgiyi topla.

---

## ADIM 1: Complexity Classification (Ilk 5 saniye)

Kullanici istegi geldiginde, asagidaki tabloya gore HEMEN siniflandir:

### Tier 1 - TRIVIAL (Hizli isler)
| Sinyal | Ornek |
|--------|-------|
| Tek dosya degisikligi | "Bu fonksiyonun adini degistir" |
| Basit git islemleri | "Push et", "Branch olustur" |
| Bilgi sorusu | "Bu dosya ne yapiyor?" |
| Formatlama/lint | "Kodu formatla" |
| Kucuk fix | "Bu typo'yu duzelt" |

**Eylem:**
- Reasoning effort: LOW
- Tool call sayisi: 1-3 max
- Subagent KULLANMA, direkt yap
- Aciklama kisalt, sonuc odakli ol

---

### Tier 2 - STANDARD (Normal isler)
| Sinyal | Ornek |
|--------|-------|
| Multi-file edit | "Bu feature'a yeni bir endpoint ekle" |
| Bug fix (bilinen) | "Bu crash'i duzelt" |
| Yeni view/component | "Login ekrani olustur" |
| Test yazimi | "Bu service icin unit test yaz" |
| Refactoring (dar kapsamli) | "Bu ViewModel'i MVVM'e cevir" |

**Eylem:**
- Reasoning effort: MEDIUM
- Todo list OLUSTUR
- Bagimsiz isler icin `general` subagent paralel kullan
- Skill referanslari:
  - Yeni modül → `ios-tuist-architect`
  - Test → `tdd-workflow`
  - Kod kalitesi → `code-reviewer`

---

### Tier 3 - COMPLEX (Agir isler)
| Sinyal | Ornek |
|--------|-------|
| Yeni modul/kit | "LocalizationKit olustur" |
| Arsitektur degisikligi | "Dependency injection yapisini degistir" |
| Multi-modul refactoring | "Tum modullerde navigation'i degistir" |
| Sistem tasarimi | "Analytics SDK tasarla" |
| Cross-cutting concern | "Tum feature'lara error handling ekle" |

**Eylem:**
- Reasoning effort: HIGH (thinking model)
- MUTLAKA `brainstorming` skill ile basla (kullanici izin verirse atla)
- Todo list DETAYLI olustur
- `general` subagent'lari PARALEL dagit
- Skill referanslari:
  - Tasarim → `brainstorming` + `senior-architect`
  - Modul → `ios-tuist-architect`
  - Kod → `tdd-workflow` + `code-reviewer`
  - UI → `ui-ux-pro-max` + `mobile-design`

---

## ADIM 2: Agent Dagilimi (Tier 2-3 icin)

### Paralel Agent Stratejisi

Bir task birden fazla bagimsiz alt-ise bolunebiliyorsa, `general` subagent'lari PARALEL calistir:

```
Ornek: "ConsentFeature'a yeni bir ekran ekle ve testlerini yaz"

Yanlis (sirayla):
  1. Explore codebase → 2. Write view → 3. Write viewmodel → 4. Write tests

Dogru (paralel):
  Subagent A: Explore codebase + Write view + viewmodel
  Subagent B: Write tests (interface'den mock'lara bakarak)
  Ana agent: Sonuclari birlesitir, integration kontrol eder
```

### Agent Rolleri

| Gorev | Agent Tipi | Kullan |
|-------|-----------|--------|
| Dosya arama/kesfetme | `explore` | Codebase sorusu, dosya bulma |
| Kod yazma | `general` | Feature impl, bug fix |
| Test yazma | `general` | Unit test, mock olusturma |
| Kod review | `general` | PR review, kalite kontrol |
| Tasarim/arsitektur | Ana agent | Brainstorm, karar verme |

---

## ADIM 3: Skill Secimi

Task tipine gore otomatik skill referans et:

| Task Tipi | Birincil Skill | Ikincil Skill |
|-----------|---------------|---------------|
| Yeni modul olustur | `ios-tuist-architect` | `senior-architect` |
| UI component | `ui-ux-pro-max` | `mobile-design` |
| Bug fix | `crash-safety` | `code-reviewer` |
| Test yaz | `tdd-workflow` | - |
| Git push | `git-pushing` | - |
| Refactoring | `code-reviewer` | `senior-architect` |
| Yeni feature tasarimi | `brainstorming` | `senior-architect` |
| Swift 6 uyumluluk | `ios-swift6-master` | - |
| Dokumantasyon | `docs-writer` | - |
| Tema/styling | `theme-factory` | `ui-ux-pro-max` |

---

## ADIM 4: Workflow Tetikleme

Eger kullanici istegi bir workflow'a tam eslesiyorsa, workflow'u dogrudan calistir:

| Anahtar Kelimeler | Workflow |
|-------------------|----------|
| "push", "commit and push", "push et" | `smart_push` |
| "build", "derle", "xcodebuild" | `verify_build` |
| "xcframework", "SDK build" | `build_xcframework` |
| "swagger", "API generate" | `generate_from_swagger` |
| "yeni modul", "kit olustur", "feature olustur" | `new_tuist_module` |
| "brainstorm", "tasarla", "fikir" | `brainstorm` |

---

## Anti-Pattern'ler (YAPMA)

1. **Gereksiz explore**: Dosya yolunu zaten biliyorsan tekrar arama
2. **Sirayla tool call**: `git status` + `git diff` + `git log` → TEK mesajda paralel gonder
3. **Over-read**: 50 satirlik dosyayi anlamak icin 10 dosya daha okuma
4. **Uzun aciklama**: Tier 1 task'lar icin 3 paragraf yazma, 1 cumle yeterli
5. **Gereksiz onay**: Basit isler icin kullaniciya soru sorma, yap ve goster
6. **Context kirliligi**: Buyuk dosyalari ana agent'ta okuma, `explore` subagent kullan

---

## Ornek: Optimum Akim

```
Kullanici: "TextKit'e yeni bir font style ekle"

1. Classify → Tier 2 (Standard, tek modul, multi-file)
2. Skill → ui-ux-pro-max + ios-tuist-architect referans
3. Plan:
   - Todo: [Interface'e enum ekle, Implementation'a logic ekle, Example'a ornek ekle]
4. Execute:
   - Paralel oku: StyledText.swift + TextKitInterface.swift
   - Paralel yaz: Her iki dosyayi da ayni mesajda edit et
5. Verify: Kullaniciya sonucu goster (3 tool call toplam)
```
