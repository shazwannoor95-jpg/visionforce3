import React from 'react';
import {AbsoluteFill, Composition, Sequence, registerRoot, useCurrentFrame, spring, useVideoConfig} from 'remotion';
type Scene = {text: string; page: number};
type Props = {scenes: Scene[]};
const Card = ({text, page}: Scene) => {
 const frame = useCurrentFrame(); const {fps} = useVideoConfig();
 const enter = spring({frame, fps, config: {damping: 18}});
 return <AbsoluteFill style={{background: '#0a1024', color: '#eef5ff', padding: 130, fontFamily: 'sans-serif', justifyContent: 'center'}}>
  <div style={{position:'absolute', right: -50, top:120, width:600, height:600, border:'5px solid #25d9bd', borderRadius:70, transform:`rotate(${frame*.45}deg)`,opacity:.3}}/>
  <div style={{fontSize:28,color:'#25d9bd',letterSpacing:6,marginBottom:45}}>VISIONFORGE 3 · HALAMAN {page}</div>
  <div style={{fontSize:62,lineHeight:1.35,maxWidth:1500,opacity:enter,transform:`translateY(${(1-enter)*60}px)`}}>{text}</div>
  <div style={{position:'absolute',left:130,bottom:130,height:8,width:1660*Math.min(frame/89,1),background:'#25d9bd'}}/>
 </AbsoluteFill>;
};
const Document = ({scenes}: Props) => <AbsoluteFill>{scenes.map((s,i)=><Sequence key={i} from={i*90} durationInFrames={90}><Card {...s}/></Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="Document" component={Document} width={1920} height={1080} fps={30} durationInFrames={90}
 defaultProps={{scenes:[{text:'Dokumen sumber',page:1}]}} calculateMetadata={({props})=>({durationInFrames:props.scenes.length*90})}/>);
