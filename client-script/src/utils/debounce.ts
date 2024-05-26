export const debounce = (func: Function, delay: number) => {
    let timeoutId: number;

    return function () {
        const args = arguments;

        clearTimeout(timeoutId);
        timeoutId = setTimeout(function () {
            // @ts-ignore
            func.apply(this, args);
        }, delay);
    };
};
