import { useState, useEffect } from "preact/hooks";
import { useLocalStorage } from "react-use";
import { TestFrequency, TestFrequencyOptions, TestRecorderState } from "./types";
import "./recorder.css";

export function PaparazziRecorder() {
    const [recorderState, setRecorderState] = useLocalStorage("pprz-recorder-state", TestRecorderState.IDLE);
    const [testName, setTestName] = useLocalStorage("pprz-recorder-test-name", "");
    const [testFrequency, setTestFrequency] = useLocalStorage("pprz-recorder-test-frequency", TestFrequency.DAILY);
    const [IsSettingsOpen, setIsSettingsOpen] = useState(false);

    useEffect(() => {
        if (recorderState === TestRecorderState.RECORDING) {
            setIsSettingsOpen(false);
        }
    }, [recorderState]);

    const startTest = () => {
        setRecorderState(TestRecorderState.RECORDING);
    };

    const stopTest = () => {
        setRecorderState(TestRecorderState.IDLE);
        setTestName("");
    };

    const handleSettingsSubmit = (e: SubmitEvent) => {
        e.preventDefault();
        setIsSettingsOpen(false);
    };

    return (
        <div className="pprz-recorder">
            <p className="pprz-title">PAPARAZZI</p>
            <div className="pprz-buttons">
                {recorderState !== TestRecorderState.LOADING && (
                    <div id="pprz-loading-overlay">
                        <span className="loader"></span>
                    </div>
                )}

                {recorderState === TestRecorderState.IDLE && (
                    <button id="pprz-start-btn" onClick={startTest}>
                        <span className="icon">&#9658;</span>
                        Start
                    </button>
                )}

                {recorderState === TestRecorderState.RECORDING && (
                    <button id="pprz-stop-btn" onClick={stopTest}>
                        <span className="icon" style="color: red; line-height: 0">
                            &#9673;
                        </span>
                        Stop
                    </button>
                )}

                <button
                    id="pprz-settings-btn"
                    onClick={() => setIsSettingsOpen(!IsSettingsOpen)}
                    disabled={recorderState === TestRecorderState.RECORDING}
                >
                    <span className="icon" style="font-size: 1.6rem; line-height: 0">
                        &#9881;
                    </span>
                    Settings
                </button>
                <div id="pprz-settings" className={IsSettingsOpen ? "open" : ""}>
                    <form id="pprz-settings-form" onSubmit={handleSettingsSubmit}>
                        <input
                            type="text"
                            id="pprz-test-name"
                            placeholder="Test name"
                            value={testName}
                            onInput={e => setTestName(e.currentTarget.value)}
                        />
                        <label for="pprz-test-frequency">Test run frequency</label>
                        <select
                            id="pprz-test-frequency"
                            onChange={e => setTestFrequency(e.currentTarget.value as TestFrequency)}
                        >
                            {TestFrequencyOptions.map(option => (
                                <option value={option} selected={testFrequency === option}>
                                    {option}
                                </option>
                            ))}
                        </select>
                    </form>
                </div>
            </div>
        </div>
    );
}
