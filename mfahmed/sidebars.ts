import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar for the Physical AI & Humanoid Robotics textbook
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Foundation Robotics Education',
      items: [
        'introduction',
        'embodied-intelligence',
        'perception-cognition-action'
      ],
    },
    {
      type: 'category',
      label: 'Simulation-Based Learning',
      items: [
        'Chapter 3 Robot Simulations With Gazebo',
        'unity-simulations',
        'Chapter 4 NVIDIA Isaac Platform'
      ],
    },
    {
      type: 'category',
      label: 'Integrated Practical Application',
      items: [
        'curriculum-overview',
        'exercises'
      ],
    },
  ],
};
export default sidebars;
