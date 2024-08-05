import 'vite/modulepreload-polyfill';
import '../css/style.css'
import typescriptLogo from '../../public/icons/typescript.svg'
import viteLogo from '../../public/icons//vite.svg'
import djangoLogo from '../../public/icons/django.svg'
import { setupCounter } from './counter.ts'

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
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
      Click on the logos to learn more. Sasha dura pidor koziol mudila
    </p>
  </div>
`

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)
