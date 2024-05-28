import html2canvas from "html2canvas";

export const takeScreenshot = async () => {
    const canvas = await html2canvas(document.body, {
        useCORS: true,
        allowTaint: true,
        windowWidth: window.innerWidth,
        windowHeight: window.innerHeight,
        x: window.scrollX,
        y: window.scrollY,
        width: window.innerWidth,
        height: window.innerHeight,
    })
    const dataURL = canvas.toDataURL("image/png");
    return dataURLtoFile(dataURL, "screenshot.png");

};

const dataURLtoFile = (dataurl: string, filename: string) => {
    var arr = dataurl.split(","),
        // @ts-ignore
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[arr.length - 1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
};
