# Karakeep Engine for SearXNG

Results are displayed as info boxes on the right.

![image](https://github.com/user-attachments/assets/3b05c4a2-35c5-4b3f-a90b-eb479ea32854)

## How to Install

- Copy this file to your `searx/engines/` directory.
- Add the following line to your `settings.yml` file under the `engines:` section:

  ```yaml
  - name: karakeep
    engine: karakeep
    shortcut: kr
    base_url: "https://your_karakeep_instance.com/"
    number_of_results: 3
    timeout: 3.0
    api_key: "YOUR_API_KEY"
  ```

You can obtain an API key under your Karakeep user settings > API Keys.
