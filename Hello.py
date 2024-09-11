# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Govt of Punjab - Smart Competency Diagnostic and Candidate Profile Score Calculator",
        page_icon="📊",
    )

    st.write("# Welcome to Govt of Punjab - Smart Competency Diagnostic and Candidate Profile Score Calculator 📊")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        This website is a prototype developed for the **Smart India Hackathon**.
        It is designed to assess candidate profiles and diagnose competency gaps.

        **👈 Select a demo from the sidebar** to see some examples
        of how it works!
        
        ### Want to learn more?
        - Check out [Smart India Hackathon](https://www.sih.gov.in/sih2024PS?technology_bucket=QWxs&category=U29mdHdhcmU=&organization=QWxs&organization_type=Mg==)

        ### See the code behind it
        - Github [Github](https://github.com/justinEapen/mentalhealth)
    """
    )


if __name__ == "__main__":
    run()
