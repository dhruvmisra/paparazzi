import { TestRecorderState, TestFrequency } from "../types";

export class TestRecorder {
    id: string;
    storage: Storage;
    storageKey: string;
    #state: TestRecorderState;
    #testName: string;
    #testFrequency: TestFrequency;

    constructor(storage: Storage, storageKey: string = "pprzTestRecorder") {
        this.storage = storage;
        this.storageKey = storageKey;
        let obj: any = {};
        const persistedRunner = this.storage.getItem(this.storageKey);
        if (persistedRunner !== null) {
            obj = JSON.parse(persistedRunner);
        }

        this.id = obj.id ?? this.generateId();
        this.#testName = obj.testName ?? "";
        this.#testFrequency = obj.testFrequency ?? TestFrequency.DAILY;
        this.render();
        this.state = obj.state ?? TestRecorderState.IDLE;
    }

    get state(): TestRecorderState {
        return this.#state;
    }

    set state(state: TestRecorderState) {
        this.#state = state;
        this.persist();
        switch (state) {
            case TestRecorderState.LOADING:
                document.getElementById("pprz-loading-overlay")?.style.setProperty("display", "block");
                break;
            case TestRecorderState.RECORDING:
                document.getElementById("pprz-loading-overlay")?.style.setProperty("display", "none");
                document.getElementById("pprz-settings-btn")?.setAttribute("disabled", "true");
                document.getElementById("pprz-start-btn")?.style.setProperty("display", "none");
                document.getElementById("pprz-stop-btn")?.style.setProperty("display", "block");
                document.getElementById("pprz-settings")?.style.setProperty("display", "none");
                break;
            case TestRecorderState.IDLE:
                document.getElementById("pprz-loading-overlay")?.style.setProperty("display", "none");
                document.getElementById("pprz-settings-btn")?.removeAttribute("disabled");
                document.getElementById("pprz-start-btn")?.style.setProperty("display", "block");
                document.getElementById("pprz-stop-btn")?.style.setProperty("display", "none");
                break;
        }
    }

    get testName(): string {
        return this.#testName;
    }

    set testName(name: string) {
        this.#testName = name;
        this.persist();
    }

    get testFrequency(): TestFrequency {
        return this.#testFrequency;
    }

    set testFrequency(frequency: TestFrequency) {
        this.#testFrequency = frequency;
        this.persist();
    }

    generateId(): string {
        return "recorder-" + Math.random().toString(36).substring(7);
    }

    persist() {
        const obj = {
            id: this.id,
            state: this.#state,
            testName: this.testName,
            testFrequency: this.testFrequency,
        };
        this.storage.setItem(this.storageKey, JSON.stringify(obj));
    }

    render() {
        const el = document.createElement("div");
        el.id = "pprz-recorder";
        el.setAttribute("data-html2canvas-ignore", "true");
        el.innerHTML = `
      <style>
        .pprz-recorder {
          position: fixed;
          bottom: 20px;
          left: 50%;
          transform: translateX(-50%);
          padding: 6px;
          border-radius: 12px;
          background-color: #020617;
          /* opacity: 0.4; */
          transition: opacity 0.2s;
        }
        .pprz-recorder:hover {
          opacity: 1;
        }
        .pprz-title {
          color: #94a3b8;
          text-align: center;
          font-family: monospace;
          margin-bottom: 4px;
          margin-top: 0;
        }
        .pprz-buttons {
          display: flex;
          justify-content: center;
          align-items: center;
          position: relative;
          gap: 6px;
        }
        .pprz-recorder button {
          color: white;
          background-color: #1e293b;
          border: none;
          padding: 0.8rem 1.2rem;
          font-size: 1.1rem;
          border-radius: 6px;
          cursor: pointer;
        }
        .pprz-recorder button:hover {
          background-color: #475569;
        }
        .pprz-recorder button:disabled {
          background-color: transparent;
          color: #475569;
          cursor: not-allowed;
        }
        #pprz-loading-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0, 0, 0, 0.8);
          z-index: 1000;
          display: none;
        }
        #pprz-loading-overlay .loader {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 2rem;
          height: 2rem;
          border: 2px solid #ffffff;
          border-bottom-color: transparent;
          border-radius: 50%;
          display: inline-block;
          box-sizing: border-box;
          animation: pprz-loader-rotation 1s linear infinite;
        }
        @keyframes pprz-loader-rotation {
          0% {
              transform: translate(-50%, -50%) rotate(0deg);
          }
          100% {
              transform: translate(-50%, -50%) rotate(360deg);
          }
        }

        #pprz-settings {
          position: absolute;
          bottom: 100%;
          right: 0;
          background-color: #020617;
          border: 1px solid #1e293b;
          border-radius: 6px;
          padding: 6px;
        }
        #pprz-settings form {
          display: flex;
          flex-direction: column;
          gap: 6px;
          color: white;
        }
        #pprz-settings input, #pprz-settings select {
          background-color: #1e293b;
          color: white;
          border: none;
          padding: 0.4rem 0.6rem;
          border-radius: 4px;
        }
        #pprz-settings label {
          font-family: sans-serif;
          margin-top: 12px;
          font-size: 0.8rem;
        }
      </style>
      <div class="pprz-recorder">
        <p class="pprz-title">PAPARAZZI</p>
        <div class="pprz-buttons">
          <div id="pprz-loading-overlay">
            <span class="loader"></span>
          </div>

          <button id="pprz-start-btn">
            <span class="icon">&#9658;</span>
            Start
          </button>
          <button id="pprz-stop-btn" style="display: none">
            <span class="icon" style="color: red; line-height: 0">&#9673;</span>
            Stop
          </button>

          <button id="pprz-settings-btn">
            <span class="icon" style="font-size: 1.6rem; line-height: 0">&#9881;</span>
            Settings
          </button>
          <div id="pprz-settings" style="display: none">
            <form id="pprz-settings-form">
              <input type="text" id="pprz-test-name" placeholder="Test name" value="${this.testName}">
              <label for="pprz-test-frequency">Test run frequency</label>
              <select id="pprz-test-frequency">
                <option value="DAILY" ${this.testFrequency == "DAILY" ? "selected" : null}>Daily</option>
                <option value="WEEKLY" ${this.testFrequency == "WEEKLY" ? "selected" : null}>Weekly</option>
              </select>
            </form>
          </div>
        </div>
      </div>
    `;
        document.body.appendChild(el);
        // Click event listeners
        document.getElementById("pprz-start-btn")?.addEventListener("click", this.startTest.bind(this));
        document.getElementById("pprz-stop-btn")?.addEventListener("click", this.stopTest.bind(this));
        document.getElementById("pprz-settings-btn")?.addEventListener("click", this.toggleSettings.bind(this));
        // Form event listeners
        document.getElementById("pprz-settings-form")?.addEventListener("submit", event => event.preventDefault());
        document.getElementById("pprz-test-name")?.addEventListener("input", this.handleNameChange.bind(this));
        document
            .getElementById("pprz-test-frequency")
            ?.addEventListener("change", this.handleFrequencyChange.bind(this));
    }

    startTest() {
        this.state = TestRecorderState.RECORDING;
    }

    stopTest() {
        this.state = TestRecorderState.IDLE;
    }

    toggleSettings() {
        const settings = document.getElementById("pprz-settings");
        if (settings) {
            if (settings.style.display === "block") {
                settings.style.display = "none";
            } else {
                settings.style.display = "block";
            }
        }
    }

    handleNameChange(event: Event) {
        const target = event.target as HTMLInputElement;
        this.testName = target.value;
    }

    handleFrequencyChange(event: Event) {
        const target = event.target as HTMLSelectElement;
        this.testFrequency = target.value as TestFrequency;
    }
}
