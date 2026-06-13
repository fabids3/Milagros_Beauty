/* ============================================================================
 * _session_patch.js — PARCHE PARA INCLUIR COOKIES DE SESIÓN EN TODO fetch()
 * ----------------------------------------------------------------------------
 * Por qué existe:
 *   El frontend original usa fetch() sin la opción `credentials: "include"`.
 *   Sin esa opción, las cookies de sesión NO se envían al backend en algunos
 *   navegadores cuando el origen es distinto (CORS) o cuando hay HTTPS.
 *
 *   Este parche envuelve la función global fetch() para añadir
 *   `credentials: "same-origin"` por defecto, sin tocar el resto del código.
 *
 *   Debe cargarse ANTES de los demás scripts (orden en las plantillas HTML).
 * ============================================================================ */
(function () {
  const _fetchOriginal = window.fetch;
  window.fetch = function (input, init) {
    init = init || {};
    if (!("credentials" in init)) {
      init.credentials = "same-origin";
    }
    return _fetchOriginal.call(this, input, init);
  };
})();
