import { useState } from 'react'

function Row(props) {
    return (
        <div className='py-7 px-10 bg-[#F65F6F] rounded-2xl text-white'>
            <div className='flex md:flex-row gap-12'>
                <div className='w-[70px] h-[70px]'>
                    <img src="src/assets/niw.png" alt="niw" />
                </div>
                <div className='flex flex-col gap-[6px]'>
                    <h1 className='font-bold text-xl'>{props.title}</h1>
                    <h2 className='text-xs'>{props.description}</h2>
                </div>
            </div>
        </div>
    )
}
export default Row
