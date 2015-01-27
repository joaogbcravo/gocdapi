"""
A selection of pipeline objects used in testing.
"""

EMPTY_PIPELINE = '''\
<pipeline name="%s">
  <materials>
    <git url="git://127.0.0.1/precommit.git"/>
  </materials>
  <stage name="stage1">
    <environmentvariables>
      <variable name="PYTHONUNBUFFERED">
        <value>1</value>
      </variable>
    </environmentvariables>
    <jobs>
      <job name="job1">
        <tasks>
          <exec command="python">
            <arg>foo.py</arg>
            <runif status="passed"/>
          </exec>
        </tasks>
      </job>
    </jobs>
  </stage>
  <stage name="stage2">
    <environmentvariables>
      <variable name="PYTHONUNBUFFERED">
        <value>True</value>
      </variable>
    </environmentvariables>
    <jobs>
      <job name="job1">
        <tasks>
          <exec command="python">
            <arg>bar.py</arg>
            <runif status="passed"/>
          </exec>
        </tasks>
      </job>
    </jobs>
  </stage>
</pipeline>
'''.strip()


UPDATED_PIPELINE = '''\
<pipeline name="%s">
  <materials>
    <git url="git://127.0.0.1/precommit.git"/>
  </materials>
  <stage name="super_stage">
    <environmentvariables>
      <variable name="PYTHONUNBUFFERED">
        <value>1</value>
      </variable>
    </environmentvariables>
    <jobs>
      <job name="job1">
        <tasks>
          <exec command="python">
            <arg>foo.py</arg>
            <runif status="passed"/>
          </exec>
        </tasks>
      </job>
    </jobs>
  </stage>
</pipeline>
'''.strip()