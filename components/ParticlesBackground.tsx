import React, { useCallback } from "react";
import Particles, { Container, IParticlesParams } from "react-tsparticles";
import { loadFull } from "tsparticles";
import { Engine } from "tsparticles-engine";

interface ParticlesBackgroundProps {
  id?: string;
  options?: IParticlesParams;
}

export const ParticlesBackground: React.FC<ParticlesBackgroundProps> = ({
  id = "tsparticles",
  options = {
    background: {
      color: {
        value: "#0d47a1",
      },
    },
    fpsLimit: 60, // reduce fps to slow down particles
    interactivity: {
      events: {
        onClick: {
          enable: true,
          mode: "push",
        },
        onHover: {
          enable: true,
          mode: "repulse",
        },
        resize: true,
      },
      modes: {
        push: {
          quantity: 4,
        },
        repulse: {
          distance: 200,
          duration: 0.4,
        },
      },
    },
    particles: {
      color: {
        value: "#ffffff",
      },
      links: {
        color: "#ffffff",
        distance: 150,
        enable: true,
        opacity: 0.5,
        width: 1,
      },
      collisions: {
        enable: true,
      },
      move: {
        direction: "none",
        enable: true,
        outModes: {
          default: "bounce",
        },
        random: false,
        speed: 2, // reduce speed to slow down particles
        straight: false,
      },
      number: {
        density: {
          enable: true,
          area: 800,
        },
        value: 80,
      },
      opacity: {
        value: 0.5,
      },
      shape: {
        type: "circle",
      },
      size: {
        value: { min: 1, max: 5 },
      },
    },
    detectRetina: true,
  },
}) => {
  const particlesInit = useCallback(async (engine: Engine) => {
    await loadFull(engine);
  }, []);

  const particlesLoaded = useCallback(async (container: Container) => {
    console.log(container);
  }, []);

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        zIndex: -1, // set z-index to -1 to push the particles to the back
      }}
    >
      <Particles
        id={id}
        init={particlesInit}
        loaded={particlesLoaded}
        options={options}
      />
    </div>
  );
};
