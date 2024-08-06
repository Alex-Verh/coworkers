import "vite/modulepreload-polyfill";
import "../css/index.css";
import typescriptLogo from "../../public/icons/typescript.svg";
import viteLogo from "../../public/icons//vite.svg";
import djangoLogo from "../../public/icons/django.svg";

document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
  <div>
    <a href="https://www.djangoproject.com/" target="_blank">
      <img src="${djangoLogo}" class="logo" alt="Django logo" />
    </a>
    <a href="https://vitejs.dev" target="_blank">
      <img src="${viteLogo}" class="logo" alt="Vite logo" />
    </a>
    <a href="https://www.typescriptlang.org/" target="_blank">
      <img src="${typescriptLogo}" class="logo vanilla" alt="TypeScript logo" />
    </a>
    <h1>Django + Vite + TypeScript</h1>
    <div class="card">
      <button id="counter" type="button"></button>
    </div>
    <p class="read-the-docs">
      Denchik bomjixa obossanaya. Evo ebali musora.
    </p>
  </div>
`;

function setupCounter(element: HTMLButtonElement) {
  let counter = 0;
  const setCounter = (count: number) => {
    counter = count;
    element.innerHTML = `Like (${counter})`;
  };
  element.addEventListener("click", () => setCounter(counter + 1));
  setCounter(0);
}
setupCounter(document.querySelector<HTMLButtonElement>("#counter")!);
