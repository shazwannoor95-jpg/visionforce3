import React from 'react';
import {AbsoluteFill, Composition, registerRoot, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';
const Motion = () => {
 const frame = useCurrentFrame(); const {fps} = useVideoConfig();
 const reveal = spring({frame, fps, config: {damping: 18}});
 return <AbsoluteFill style={{background:'#090e20',color:'#eef5ff',fontFamily:'sans-serif',justifyContent:'center',padding:140}}>
  <div style={{position:'absolute',width:700,height:700,border:'3px solid #2ae6c8',borderRadius:90,right:-70,top:160,transform:`rotate(${frame * 0.7}deg)`,opacity:0.4}} />
  <div style={{color:'#2ae6c8',fontSize:30,letterSpacing:10,marginBottom:30}}>MOTION ENGINE / 01</div>
  <div style={{fontSize:130,fontWeight:800,transform:`translateY(${(1-reveal)*90}px)`,opacity:reveal}}>VISIONFORGE 3</div>
  <div style={{fontSize:42,marginTop:30,opacity:interpolate(frame,[20,45],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>Ideas in motion.</div>
  <div style={{position:'absolute',left:140,bottom:140,height:8,width:interpolate(frame,[0,119],[0,1640]),background:'#2ae6c8'}} />
  <div style={{position:'absolute',right:140,bottom:170,fontSize:24}}>1920 × 1080 / 30 FPS</div>
 </AbsoluteFill>;
};
registerRoot(() => <Composition id="VisionForge3" component={Motion} durationInFrames={120} fps={30} width={1920} height={1080}/>);
