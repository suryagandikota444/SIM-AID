import { faArrowRightLong, faUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React, { useState } from "react";
import { Dna } from 'react-loader-spinner'

import 'react-spinner-animated/dist/index.css'


export default function Home() {
  const hiddenFileInput = React.useRef(null);
  const [loading, setLoading] = useState("not_loading");
  const [fileName, setFileName] = useState("");

  const handleClick = (event:any) => {
    hiddenFileInput.current.click();
  };

  const handleChange = (event:any) => {
    setLoading("loading")
    const fileUploaded = event.target.files[0];
    setFileName(fileUploaded.name)
    const formData = new FormData();
    formData.append('file', fileUploaded);  
    fetch('http://127.0.0.1:5001/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      setLoading("loading_complete")
    })
    .catch(error => {
      console.log(error)
    });
  };
  
  return (
    <div className="flex bg-gradient-to-b from-cyan-500 to-blue-500 h-screen justify-center content-center place-content-center">
      <div className="w-96 rounded overflow-hidden shadow-xl h-96 mt-36 flex justify-center content-center backdrop-blur-lg bg-white/30">
        <div className="px-6 py-4 mt-24">
          <div className="text-black text-center text-6xl font-extrabold mb-4 text-white">
            SIM-AID
          </div>
          <div className="font-semibold text-xl mb-2 text-black text-center">Please enter new image</div>
          <div className="flex justify-center">
            {loading == "loading" ? 
                <Dna
                visible={true}
                height="60"
                width="60"
                ariaLabel="dna-loading"
                wrapperStyle={{}}
                wrapperClass="dna-wrapper"
              />: loading=="loading_complete" ? 
                <div className="flex-row">
                  <button type="button" 
                    className="inline-block px-4 pt-2.5 pb-2 bg-blue-600 text-white font-medium text-xs leading-normal uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out flex align-center"
                    >
                    <Link href={{pathname: "/output", query: fileName}}>
                      Run Analysis
                    </Link>
                    <FontAwesomeIcon icon={faArrowRightLong} className=" ml-2" size="lg"/>
                  </button>
                  <input type="file" style={{display:'none'}} ref={hiddenFileInput} onChange={handleChange}/>
                </div> : <div className="flex space-x-2 justify-center">
                <div className="flex-row">
                  <button type="button" 
                    className="inline-block px-4 pt-2.5 pb-2 bg-blue-600 text-white font-medium text-xs leading-normal uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out flex align-center"
                    onClick={handleClick}
                    >
                    Enter Image
                  <FontAwesomeIcon icon={faUpload} className=" ml-2" size="lg"/>
                  </button>
                  <input type="file" style={{display:'none'}} ref={hiddenFileInput} onChange={handleChange}/>
                </div>
              </div>}
          </div>
        </div>
      </div>
    </div>
  )
}
