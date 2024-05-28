# Paparazzi client-side script

This is a client-side script that can be added to any website to show the paparazzi popup UI and to start recording tests.

## How to use it?

For a new website in a non-production environment, add it as a script in the end of body.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Paparazzi</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="https://paparazzi.dhruvmisra.com/paparazzi-client.mjs"></script>
  </body>
</html>
```

For an existing website, add this block of code in the console.

```js
(function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)){ return; }
    js = d.createElement(s); js.id = id;
    js.src = "https://paparazzi.dhruvmisra.com/paparazzi-client.mjs";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'paparazzi-client'));
```


### Note

Functioning of the script is heavily dependent on the CSP policy of the website.

## Development

This project uses `pnpm` for dependency management.

Install dependencies

```bash
pnpm install
```

Start development server

```bash
pnpm dev
```

Build final bundle

```bash
pnpm build
```
