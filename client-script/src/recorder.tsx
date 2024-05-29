import { useState, useEffect, useRef, useCallback } from "preact/hooks";
import { useEffectOnce, useLocalStorage } from "react-use";
import { TestFrequency, TestFrequencyOptions, TestRecorderState } from "./types";
import { constructClickStep, constructScrollStep, CreateTest, CreateTestStep } from "./services";
import { debounce } from "./utils";
import "./recorder.css";
import { CompleteTest } from "./services/test";
import { constructNavigationStep, constructScreenshotStep } from "./services/step";

export function PaparazziRecorder() {
    const [recorderState, setRecorderState] = useLocalStorage("pprz-recorder-state", TestRecorderState.IDLE);
    const [testName, setTestName] = useLocalStorage("pprz-recorder-test-name", "");
    const [testFrequency, setTestFrequency] = useLocalStorage("pprz-recorder-test-frequency", TestFrequency.DAILY);
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [isVisible, _] = useLocalStorage("pprz-recorder-visible", true);

    const [currentTestId, setCurrentTestId] = useLocalStorage("pprz-recorder-current-test-id", "");
    // Required to use testId in event listeners
    const testId = useRef(currentTestId);

    useEffectOnce(() => {
        if (recorderState === TestRecorderState.LOADING) {
            setRecorderState(TestRecorderState.IDLE);
        }
    });

    useEffect(() => {
        testId.current = currentTestId;
    }, [currentTestId]);

    useEffect(() => {
        if (recorderState === TestRecorderState.RECORDING) {
            setIsSettingsOpen(false);
            addEventListeners();
        }
        return () => {
            if (recorderState === TestRecorderState.RECORDING) {
                removeEventListeners();
            }
        };
    }, [recorderState]);

    const handleGlobalClick = useCallback(async (e: MouseEvent) => {
        if ((e.target as HTMLInputElement).id === "pprz-stop-btn") {
            return;
        }
        console.log(e);
        console.log(testId.current);
        let step = constructClickStep(testId.current!, e);
        await CreateTestStep(step);
        step = constructScreenshotStep(testId.current!);
        await CreateTestStep(step);
    }, []);

    const handleGlobalScroll = useCallback(async (e: Event) => {
        console.log(e);
        console.log(testId.current);
        let step = constructScrollStep(testId.current!, e);
        await CreateTestStep(step);
        step = constructScreenshotStep(testId.current!);
        await CreateTestStep(step);
    }, []);

    const addEventListeners = () => {
        window.debouncedScrollHandler = debounce(handleGlobalScroll, 500);
        document.addEventListener("click", handleGlobalClick);
        document.addEventListener("scroll", window.debouncedScrollHandler);
    };

    const removeEventListeners = () => {
        document.removeEventListener("click", handleGlobalClick);
        window.debouncedScrollHandler && document.removeEventListener("scroll", window.debouncedScrollHandler);
    };

    const startTest = async () => {
        setRecorderState(TestRecorderState.LOADING);
        const testData = await CreateTest(testName ?? "", testFrequency ?? TestFrequency.DAILY);
        setCurrentTestId(testData.id);
        // initial navigation step
        const navigationStep = constructNavigationStep(testData.id, window.location.href);
        await CreateTestStep(navigationStep);
        setRecorderState(TestRecorderState.RECORDING);
    };

    const stopTest = async () => {
        await CompleteTest(currentTestId!);
        setCurrentTestId("");
        setTestName("");
        setRecorderState(TestRecorderState.IDLE);
    };

    const handleSettingsSubmit = (e: SubmitEvent) => {
        e.preventDefault();
        setIsSettingsOpen(false);
    };

    return isVisible ? (
        <div className="pprz-recorder">
            <p className="pprz-title">PAPARAZZI</p>
            <div className="pprz-buttons">
                {recorderState === TestRecorderState.LOADING && (
                    <div id="pprz-loading-overlay">
                        <span className="loader"></span>
                    </div>
                )}

                {recorderState !== TestRecorderState.RECORDING && (
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
                    onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                    disabled={recorderState === TestRecorderState.RECORDING}
                >
                    <span className="icon" style="font-size: 1.6rem; line-height: 0">
                        &#9881;
                    </span>
                    Settings
                </button>
                <div id="pprz-settings" className={isSettingsOpen ? "open" : ""}>
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
    ) : <div></div>;
}
