import { render } from 'preact'
import { PaparazziRecorder } from './recorder';
import { ENABLE_MOCKING } from './config';

async function enableMocking() {
  if (!ENABLE_MOCKING) {
    return;
  }
 
  const { worker } = await import('./mocks/browser');
  return worker.start();
}

const main = () => {
  // run only on the client
  if (typeof window === 'undefined') {
    return;
  }

  const el = document.createElement("div");
  el.id = "pprz-recorder";
  el.setAttribute("data-html2canvas-ignore", "true");
  document.body.appendChild(el);

  enableMocking().then(() => {
    render(<PaparazziRecorder />, document.getElementById(el.id)!)
  })
}
main();
