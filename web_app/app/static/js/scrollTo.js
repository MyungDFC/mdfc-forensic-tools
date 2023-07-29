function scrollToElement(elementId) {
  let mainContent = document.querySelector("#main-content");
  let location = document.querySelector(elementId).offsetTop;

  mainContent.scrollTo({ top: location, behavior: "smooth" });
}
