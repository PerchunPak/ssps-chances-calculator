const daisyui = require('daisyui');
const typography = require('@tailwindcss/typography');

/** @type {import('tailwindcss').Config}*/
const config = {
	content: ['./src/**/*.{html,js,svelte,ts}'],

	theme: {
		extend: {
			fontFamily: {
				// from https://systemfontstack.com/
				sans: [
					'Roboto',
					'-apple-system',
					'BlinkMacSystemFont',
					'"avenir next"',
					'avenir',
					'"segoe ui"',
					'"helvetica neue"',
					'helvetica',
					'Cantarell',
					'Ubuntu',
					'noto',
					'arial',
					'sans-serif'
				],
				serif: [
					'"Iowan Old Style"',
					'"Apple Garamond"',
					'Baskerville',
					'"Times New Roman"',
					'"Droid Serif"',
					'Times',
					'"Source Serif Pro"',
					'serif',
					'"Apple Color Emoji"',
					'"Segoe UI Emoji"',
					'"Segoe UI Symbol"'
				],
				mono: ['Menlo', 'Consolas', 'Monaco', '"Liberation Mono"', '"Lucida Console"', 'monospace']
			}
		}
	},
	daisyui: {
		logs: false
	},

	plugins: [typography, daisyui]
};

module.exports = config;
