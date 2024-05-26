// @ts-nocheck
// https://stackoverflow.com/a/37438675/13715928
export const ObjectId = (m = Math, d = Date, h = 16, s = s => m.floor(s).toString(h)) =>
    s(d.now() / 1000) + " ".repeat(h).replace(/./g, () => s(m.random() * h));


export const generateTestId = () => "test-" + ObjectId();
export const generateTestStepId = () => "step-" + ObjectId();
export const generateTestScreenshotId = () => "screenshot-" + ObjectId();
