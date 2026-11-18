# Project ideas

[Deutsch](PROJECT-IDEAS.de.md) · [Back to my profile](README.md)

**These are ideas I might build. None of them exists yet.** I have not written code in any of the languages below, so they are not in my [tech stack](README.md). Each idea is a real problem from my own work that would be a good excuse to learn the language. If one of them becomes a repository, it moves into the profile README.

## R

- **Discord activity report**: read the statistics my Discord bots already collect and render a monthly report per channel and hour of day, with charts from ggplot2.
- **Hosting cost tracker**: import invoice CSVs from my hosting providers and show which service costs how much per month.

## MATLAB

- **Equalizer lab for VectoBeat**: design and test the equalizer presets of my music bot offline, then copy the filter coefficients into the bot. I would run it on GNU Octave, which executes most MATLAB code for free.

## Julia

- **Load-test analysis**: read the result files of my load tests and find the point where a service's response times start to climb.
- **Terrain noise experiments**: try noise functions for Minecraft-style world generation and compare their speed with the Java version.

## Scala

- **Event pipeline for game servers**: collect join, leave and chat events from a Minecraft network through Kafka and aggregate them with Apache Pekko Streams.

## Elixir

- **Live status page**: a Phoenix LiveView page that shows the health of all my services and updates without a reload.
- **Discord bot on the BEAM**: a small bot built on Nostrum, to see how Elixir handles many servers at once compared with my Python and TypeScript bots.

## Haskell

- **Config checker**: a command-line tool that parses Docker Compose and Traefik files and reports mistakes before a deploy.

## Objective-C

- **iOS share extension for Tellersonne**: save a recipe from Safari straight into the cooking app.

## VB.NET

- **Quote generator for UplyTech**: a small Windows tool that fills our quote templates from a CSV and saves them as PDF.

## Delphi / Pascal

- **Server toolbox for Windows**: a native app built with Free Pascal and Lazarus that checks ports, DNS records and TLS certificates of my servers.

## GDScript

- **LifeVerse prototype**: a small playable slice of [LifeVerse](https://github.com/VectoDE/LifeVerse) in Godot, to test the life-simulation loop before picking an engine.

## HLSL / GLSL

- **Portfolio shaders**: GLSL fragment shaders for the Three.js background of my [portfolio](https://github.com/VectoDE/Portfolio).
- **Post-process material in Unreal**: an HLSL material for a stylised look in Unreal Engine.

## Solidity

- **Certificate fingerprints**: a contract on a test network that stores the hashes of my certificate PDFs, so anyone can check that a PDF is unchanged. Test network only, no tokens.
