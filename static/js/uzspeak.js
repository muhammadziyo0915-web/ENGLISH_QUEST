/* English Quest: inglizcha so'zni O'ZBEKCHA o'qilishida, sekin va aniq aytib beradi.
   Masalan: banana -> "ba-na-na" (o'zbek ovozida). Tarjimani aytmaydi. */
(function () {
  var RATE = 0.45;          // sekinroq: 1 = oddiy tezlik, kichikroq = sekinroq
  var voicesReady = null;

  // "bə-na-nə" kabi yozuvni o'zbek lotin imlosiga o'tkazadi
  function toUzbek(guide) {
    var s = String(guide || '').toLowerCase();
    s = s.replace(/[:ː]/g, '')          // cho'ziq belgisi
         .replace(/dh/g, 'z').replace(/th/g, 's')
         .replace(/ə/g, 'a').replace(/ö/g, 'o').replace(/ɛ/g, 'e')
         .replace(/w/g, 'v')
         .replace(/[^a-z'\- ]/g, '');
    return s;
  }

  // Bo'g'inlar orasiga qisqa pauza qo'yadi: "ba, na, na"
  function toSpeech(guide) {
    return toUzbek(guide).split('-').filter(Boolean).join(', ');
  }

  function loadVoices() {
    if (voicesReady) return voicesReady;
    voicesReady = new Promise(function (resolve) {
      var v = speechSynthesis.getVoices();
      if (v.length) return resolve(v);
      speechSynthesis.addEventListener('voiceschanged', function () {
        resolve(speechSynthesis.getVoices());
      }, { once: true });
      setTimeout(function () { resolve(speechSynthesis.getVoices()); }, 1200);
    });
    return voicesReady;
  }

  function pickVoice(voices) {
    var uz = voices.filter(function (v) { return /^uz/i.test(v.lang); });
    if (uz.length) return { voice: uz[0], lang: uz[0].lang };
    // O'zbek ovozi yo'q bo'lsa, lotin imlosini to'g'ri o'qiydigan turk ovozi eng yaqin
    var tr = voices.filter(function (v) { return /^tr/i.test(v.lang); });
    if (tr.length) return { voice: tr[0], lang: tr[0].lang };
    return null;
  }

  // guide = "bə-na-nə" (talaffuz yozuvi), word = "banana" (zaxira)
  window.UzSpeak = function (guide, word) {
    if (!('speechSynthesis' in window)) return;
    speechSynthesis.cancel();
    loadVoices().then(function (voices) {
      var text = toSpeech(guide);
      var picked = pickVoice(voices);
      var u;
      if (picked && text) {
        u = new SpeechSynthesisUtterance(text);
        u.voice = picked.voice;
        u.lang = picked.lang;
      } else {
        // Hech qanday mos ovoz topilmadi: inglizcha ovozda sekin o'qiydi
        u = new SpeechSynthesisUtterance(word || text);
        u.lang = 'en-US';
      }
      u.rate = RATE;
      u.pitch = 1;
      u.volume = 1;
      speechSynthesis.speak(u);
    });
  };
})();
