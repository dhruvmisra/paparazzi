import { render } from 'preact'
import { PaparazziRecorder } from './recorder';

const main = () => {
  // run only on the client
  if (typeof window === 'undefined') {
    return;
  }

  const el = document.createElement("div");
  el.id = "pprz-recorder";
  el.setAttribute("data-html2canvas-ignore", "true");
  document.body.appendChild(el);

  render(<PaparazziRecorder />, document.getElementById(el.id)!)
}

main();
